"""
Social Media API Integration Classes for Police Monitoring
Provides standardized interfaces for multiple social media platforms
"""

import requests
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import hashlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StandardizedPost:
    """Standardized data structure for social media posts across platforms"""
    id: str
    platform: str
    content: str
    author: str
    author_id: str
    timestamp: datetime
    url: str
    engagement: Dict[str, int]  # likes, shares, comments, etc.
    hashtags: List[str]
    mentions: List[str]
    media_urls: List[str]
    location: Optional[str] = None
    language: Optional[str] = None
    verified_author: bool = False
    sentiment_score: Optional[float] = None
    threat_level: str = "low"  # low, medium, high, critical
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for easy serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

@dataclass
class APIResponse:
    """Standardized API response structure"""
    success: bool
    data: List[StandardizedPost]
    error_message: Optional[str] = None
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[datetime] = None
    total_results: Optional[int] = None
    next_page_token: Optional[str] = None

class RateLimiter:
    """Rate limiting utility for API calls"""
    
    def __init__(self, calls_per_window: int, window_seconds: int):
        self.calls_per_window = calls_per_window
        self.window_seconds = window_seconds
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove old calls outside the window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.window_seconds]
        
        if len(self.calls) >= self.calls_per_window:
            sleep_time = self.window_seconds - (now - self.calls[0])
            if sleep_time > 0:
                logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                return True
        
        self.calls.append(now)
        return False

class BaseAPIManager(ABC):
    """Abstract base class for all API managers"""
    
    def __init__(self, api_key: str, rate_limit_calls: int = 100, rate_limit_window: int = 3600):
        self.api_key = api_key
        self.rate_limiter = RateLimiter(rate_limit_calls, rate_limit_window)
        self.session = requests.Session()
        self.session.timeout = 30
    
    @abstractmethod
    def search_content(self, keywords: List[str], **kwargs) -> APIResponse:
        """Search for content by keywords"""
        pass
    
    @abstractmethod
    def get_user_content(self, user_id: str, **kwargs) -> APIResponse:
        """Get content from specific user"""
        pass
    
    def _standardize_post(self, raw_post: Dict, platform: str) -> StandardizedPost:
        """Convert platform-specific post to standardized format"""
        # This method should be overridden by each platform manager
        pass
    
    def _detect_coordinated_campaign(self, posts: List[StandardizedPost]) -> Dict[str, Any]:
        """Detect potential coordinated campaigns"""
        if len(posts) < 3:
            return {"suspicious": False, "confidence": 0.0}
        
        # Check for similar content
        content_hashes = []
        for post in posts:
            content_hash = hashlib.md5(post.content.lower().encode()).hexdigest()
            content_hashes.append(content_hash)
        
        unique_hashes = set(content_hashes)
        similarity_ratio = 1 - (len(unique_hashes) / len(content_hashes))
        
        # Check for coordinated timing
        timestamps = [post.timestamp for post in posts]
        timestamps.sort()
        time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
        avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 0
        
        # Suspicious if high similarity and coordinated timing
        confidence = (similarity_ratio * 0.6) + (min(1.0, 300 / max(avg_time_diff, 1)) * 0.4)
        
        return {
            "suspicious": confidence > 0.7,
            "confidence": confidence,
            "similarity_ratio": similarity_ratio,
            "avg_time_diff_seconds": avg_time_diff,
            "analysis": {
                "content_similarity": "High" if similarity_ratio > 0.8 else "Medium" if similarity_ratio > 0.5 else "Low",
                "timing_coordination": "High" if avg_time_diff < 300 else "Medium" if avg_time_diff < 3600 else "Low"
            }
        }

class TwitterAPIManager(BaseAPIManager):
    """Twitter API v2 Manager for police monitoring"""
    
    def __init__(self, bearer_token: str):
        super().__init__(bearer_token, rate_limit_calls=300, rate_limit_window=900)  # 300 requests per 15 minutes
        self.base_url = "https://api.twitter.com/2"
        self.session.headers.update({
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "PoliceMonitorBot/1.0"
        })
    
    def search_content(self, keywords: List[str], max_results: int = 100, **kwargs) -> APIResponse:
        """Search tweets by keywords"""
        try:
            self.rate_limiter.wait_if_needed()
            
            # Build search query
            query = " OR ".join([f'"{keyword}"' for keyword in keywords])
            if kwargs.get('exclude_retweets', True):
                query += " -is:retweet"
            
            params = {
                "query": query,
                "max_results": min(max_results, 100),
                "tweet.fields": "created_at,author_id,public_metrics,lang,geo,context_annotations",
                "user.fields": "verified,public_metrics",
                "expansions": "author_id"
            }
            
            if kwargs.get('start_time'):
                params["start_time"] = kwargs['start_time'].isoformat()
            if kwargs.get('end_time'):
                params["end_time"] = kwargs['end_time'].isoformat()
            
            response = self.session.get(f"{self.base_url}/tweets/search/recent", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_twitter_response(data)
            
            # Detect coordinated campaigns
            if len(posts) > 2:
                campaign_analysis = self._detect_coordinated_campaign(posts)
                for post in posts:
                    if campaign_analysis["suspicious"]:
                        post.threat_level = "medium" if campaign_analysis["confidence"] > 0.8 else "low"
                        if not post.metadata:
                            post.metadata = {}
                        post.metadata["campaign_analysis"] = campaign_analysis
            
            return APIResponse(
                success=True,
                data=posts,
                rate_limit_remaining=int(response.headers.get('x-rate-limit-remaining', 0)),
                total_results=data.get('meta', {}).get('result_count', 0)
            )
            
        except requests.RequestException as e:
            logger.error(f"Twitter API error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def get_user_content(self, user_id: str, max_results: int = 100, **kwargs) -> APIResponse:
        """Get user timeline"""
        try:
            self.rate_limiter.wait_if_needed()
            
            params = {
                "max_results": min(max_results, 100),
                "tweet.fields": "created_at,public_metrics,lang,geo,context_annotations",
                "exclude": "retweets" if kwargs.get('exclude_retweets', True) else None
            }
            
            response = self.session.get(f"{self.base_url}/users/{user_id}/tweets", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_twitter_response(data)
            
            return APIResponse(
                success=True,
                data=posts,
                rate_limit_remaining=int(response.headers.get('x-rate-limit-remaining', 0))
            )
            
        except requests.RequestException as e:
            logger.error(f"Twitter user timeline error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def monitor_hashtags(self, hashtags: List[str], **kwargs) -> APIResponse:
        """Monitor specific hashtags"""
        hashtag_keywords = [f"#{tag.lstrip('#')}" for tag in hashtags]
        return self.search_content(hashtag_keywords, **kwargs)
    
    def analyze_user_behavior(self, user_id: str) -> Dict[str, Any]:
        """Analyze user behavior patterns for suspicious activity"""
        try:
            # Get user info
            user_response = self.session.get(
                f"{self.base_url}/users/{user_id}",
                params={"user.fields": "created_at,public_metrics,verified"}
            )
            user_response.raise_for_status()
            user_data = user_response.json().get('data', {})
            
            # Get recent tweets
            timeline_response = self.get_user_content(user_id, max_results=100)
            
            if not timeline_response.success:
                return {"error": "Could not fetch user timeline"}
            
            posts = timeline_response.data
            
            # Analyze patterns
            analysis = {
                "user_info": {
                    "id": user_data.get('id'),
                    "username": user_data.get('username'),
                    "verified": user_data.get('verified', False),
                    "followers": user_data.get('public_metrics', {}).get('followers_count', 0),
                    "following": user_data.get('public_metrics', {}).get('following_count', 0),
                    "account_age_days": (datetime.now() - datetime.fromisoformat(user_data.get('created_at', '').replace('Z', '+00:00'))).days if user_data.get('created_at') else 0
                },
                "posting_patterns": {
                    "total_posts": len(posts),
                    "avg_engagement": sum(p.engagement.get('total', 0) for p in posts) / len(posts) if posts else 0,
                    "languages": list(set(p.language for p in posts if p.language)),
                    "hashtag_usage": sum(len(p.hashtags) for p in posts) / len(posts) if posts else 0
                },
                "suspicious_indicators": []
            }
            
            # Check for suspicious patterns
            if analysis["user_info"]["account_age_days"] < 30:
                analysis["suspicious_indicators"].append("New account (< 30 days)")
            
            if analysis["posting_patterns"]["total_posts"] > 50 and analysis["posting_patterns"]["avg_engagement"] < 2:
                analysis["suspicious_indicators"].append("High volume, low engagement")
            
            follower_following_ratio = analysis["user_info"]["followers"] / max(analysis["user_info"]["following"], 1)
            if follower_following_ratio < 0.1 and analysis["user_info"]["following"] > 1000:
                analysis["suspicious_indicators"].append("Unusual follower/following ratio")
            
            return analysis
            
        except Exception as e:
            logger.error(f"User behavior analysis error: {str(e)}")
            return {"error": str(e)}
    
    def _process_twitter_response(self, data: Dict) -> List[StandardizedPost]:
        """Process Twitter API response into standardized format"""
        posts = []
        tweets = data.get('data', [])
        users = {user['id']: user for user in data.get('includes', {}).get('users', [])}
        
        for tweet in tweets:
            author_id = tweet.get('author_id')
            author_info = users.get(author_id, {})
            
            # Extract hashtags and mentions
            hashtags = re.findall(r'#(\w+)', tweet.get('text', ''))
            mentions = re.findall(r'@(\w+)', tweet.get('text', ''))
            
            # Calculate total engagement
            metrics = tweet.get('public_metrics', {})
            total_engagement = (
                metrics.get('like_count', 0) + 
                metrics.get('retweet_count', 0) + 
                metrics.get('reply_count', 0) + 
                metrics.get('quote_count', 0)
            )
            
            post = StandardizedPost(
                id=tweet['id'],
                platform="twitter",
                content=tweet.get('text', ''),
                author=author_info.get('username', 'unknown'),
                author_id=author_id,
                timestamp=datetime.fromisoformat(tweet.get('created_at', '').replace('Z', '+00:00')),
                url=f"https://twitter.com/{author_info.get('username', 'unknown')}/status/{tweet['id']}",
                engagement={
                    'likes': metrics.get('like_count', 0),
                    'retweets': metrics.get('retweet_count', 0),
                    'replies': metrics.get('reply_count', 0),
                    'quotes': metrics.get('quote_count', 0),
                    'total': total_engagement
                },
                hashtags=hashtags,
                mentions=mentions,
                media_urls=[],  # Would need to process media entities
                language=tweet.get('lang'),
                verified_author=author_info.get('verified', False),
                metadata={
                    'tweet_id': tweet['id'],
                    'author_metrics': author_info.get('public_metrics', {}),
                    'context_annotations': tweet.get('context_annotations', [])
                }
            )
            posts.append(post)
        
        return posts

class FacebookAPIManager(BaseAPIManager):
    """Facebook Graph API Manager for police monitoring"""
    
    def __init__(self, access_token: str):
        super().__init__(access_token, rate_limit_calls=200, rate_limit_window=3600)  # 200 requests per hour
        self.base_url = "https://graph.facebook.com/v18.0"
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })
    
    def search_content(self, keywords: List[str], max_results: int = 100, **kwargs) -> APIResponse:
        """Search public posts (Note: Limited by Facebook's API restrictions)"""
        try:
            self.rate_limiter.wait_if_needed()
            
            # Facebook's search is very limited for public content
            # This is a placeholder implementation - actual implementation would depend on available endpoints
            posts = []
            
            logger.warning("Facebook public post search is heavily restricted. Consider using page monitoring instead.")
            
            return APIResponse(
                success=True,
                data=posts,
                error_message="Facebook public search is limited by platform restrictions"
            )
            
        except requests.RequestException as e:
            logger.error(f"Facebook API error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def get_user_content(self, user_id: str, max_results: int = 100, **kwargs) -> APIResponse:
        """Get user posts (requires appropriate permissions)"""
        try:
            self.rate_limiter.wait_if_needed()
            
            params = {
                "fields": "id,message,created_time,likes.summary(true),comments.summary(true),shares",
                "limit": min(max_results, 100)
            }
            
            response = self.session.get(f"{self.base_url}/{user_id}/posts", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_facebook_response(data)
            
            return APIResponse(
                success=True,
                data=posts,
                rate_limit_remaining=self._get_rate_limit_remaining(response)
            )
            
        except requests.RequestException as e:
            logger.error(f"Facebook user content error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def monitor_page(self, page_id: str, **kwargs) -> APIResponse:
        """Monitor Facebook page posts"""
        try:
            self.rate_limiter.wait_if_needed()
            
            params = {
                "fields": "id,message,created_time,likes.summary(true),comments.summary(true),shares,from",
                "limit": kwargs.get('max_results', 25)
            }
            
            if kwargs.get('since'):
                params['since'] = kwargs['since'].timestamp()
            if kwargs.get('until'):
                params['until'] = kwargs['until'].timestamp()
            
            response = self.session.get(f"{self.base_url}/{page_id}/posts", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_facebook_response(data)
            
            return APIResponse(
                success=True,
                data=posts,
                rate_limit_remaining=self._get_rate_limit_remaining(response)
            )
            
        except requests.RequestException as e:
            logger.error(f"Facebook page monitoring error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def analyze_engagement(self, post_id: str) -> Dict[str, Any]:
        """Analyze engagement patterns for a specific post"""
        try:
            self.rate_limiter.wait_if_needed()
            
            # Get post details
            params = {
                "fields": "id,message,created_time,likes.summary(true),comments.summary(true),shares,insights"
            }
            
            response = self.session.get(f"{self.base_url}/{post_id}", params=params)
            response.raise_for_status()
            
            post_data = response.json()
            
            # Get comments for sentiment analysis
            comments_response = self.session.get(
                f"{self.base_url}/{post_id}/comments",
                params={"fields": "message,created_time,from,like_count"}
            )
            
            comments = comments_response.json().get('data', []) if comments_response.status_code == 200 else []
            
            analysis = {
                "post_id": post_id,
                "engagement_metrics": {
                    "likes": post_data.get('likes', {}).get('summary', {}).get('total_count', 0),
                    "comments": post_data.get('comments', {}).get('summary', {}).get('total_count', 0),
                    "shares": post_data.get('shares', {}).get('count', 0)
                },
                "comment_analysis": {
                    "total_comments": len(comments),
                    "avg_comment_likes": sum(c.get('like_count', 0) for c in comments) / len(comments) if comments else 0,
                    "comment_timeline": [c.get('created_time') for c in comments]
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Facebook engagement analysis error: {str(e)}")
            return {"error": str(e)}
    
    def _process_facebook_response(self, data: Dict) -> List[StandardizedPost]:
        """Process Facebook API response into standardized format"""
        posts = []
        
        for post in data.get('data', []):
            # Extract basic engagement metrics
            likes_count = post.get('likes', {}).get('summary', {}).get('total_count', 0)
            comments_count = post.get('comments', {}).get('summary', {}).get('total_count', 0)
            shares_count = post.get('shares', {}).get('count', 0)
            
            total_engagement = likes_count + comments_count + shares_count
            
            # Extract hashtags and mentions from message
            message = post.get('message', '')
            hashtags = re.findall(r'#(\w+)', message)
            mentions = re.findall(r'@(\w+)', message)
            
            standardized_post = StandardizedPost(
                id=post['id'],
                platform="facebook",
                content=message,
                author=post.get('from', {}).get('name', 'unknown'),
                author_id=post.get('from', {}).get('id', ''),
                timestamp=datetime.fromisoformat(post.get('created_time', '').replace('Z', '+00:00')),
                url=f"https://facebook.com/{post['id']}",
                engagement={
                    'likes': likes_count,
                    'comments': comments_count,
                    'shares': shares_count,
                    'total': total_engagement
                },
                hashtags=hashtags,
                mentions=mentions,
                media_urls=[],  # Would need to process attachments
                verified_author=False,  # Would need to check page verification
                metadata={
                    'post_id': post['id'],
                    'from': post.get('from', {})
                }
            )
            posts.append(standardized_post)
        
        return posts
    
    def _get_rate_limit_remaining(self, response) -> Optional[int]:
        """Extract rate limit information from response headers"""
        # Facebook uses different header names
        return None  # Would need to implement based on actual Facebook headers

class TelegramAPIManager(BaseAPIManager):
    """Telegram Bot API Manager for police monitoring"""
    
    def __init__(self, bot_token: str):
        super().__init__(bot_token, rate_limit_calls=30, rate_limit_window=60)  # 30 requests per minute
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.bot_info = None
    
    def search_content(self, keywords: List[str], max_results: int = 100, **kwargs) -> APIResponse:
        """Search is not directly available in Telegram API - use channel monitoring"""
        logger.warning("Telegram doesn't support direct search. Use monitor_channel for specific channels.")
        return APIResponse(
            success=False,
            data=[],
            error_message="Telegram API doesn't support content search. Use channel monitoring instead."
        )
    
    def get_user_content(self, user_id: str, **kwargs) -> APIResponse:
        """Get user content is not available in Telegram API"""
        logger.warning("Telegram API doesn't support user content retrieval")
        return APIResponse(
            success=False,
            data=[],
            error_message="Telegram API doesn't support user content retrieval"
        )
    
    def monitor_channel(self, channel_username: str, **kwargs) -> APIResponse:
        """Monitor public Telegram channel"""
        try:
            self.rate_limiter.wait_if_needed()
            
            # Get channel info first
            channel_info = self._get_chat_info(channel_username)
            if not channel_info:
                return APIResponse(
                    success=False,
                    data=[],
                    error_message=f"Could not access channel: {channel_username}"
                )
            
            # Note: Telegram Bot API has limited access to channel history
            # This would require storing messages as they come through updates
            posts = []
            
            logger.info(f"Monitoring channel: {channel_username}")
            
            return APIResponse(
                success=True,
                data=posts,
                error_message="Channel monitoring requires webhook setup for real-time updates"
            )
            
        except Exception as e:
            logger.error(f"Telegram channel monitoring error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def get_bot_info(self) -> Dict[str, Any]:
        """Get bot information"""
        try:
            if not self.bot_info:
                response = self.session.get(f"{self.base_url}/getMe")
                response.raise_for_status()
                self.bot_info = response.json().get('result', {})
            
            return self.bot_info
            
        except Exception as e:
            logger.error(f"Failed to get bot info: {str(e)}")
            return {}
    
    def detect_bot_activity(self, messages: List[Dict]) -> Dict[str, Any]:
        """Detect potential bot activity in messages"""
        if not messages:
            return {"bot_detected": False, "confidence": 0.0}
        
        # Analyze message patterns
        time_intervals = []
        for i in range(1, len(messages)):
            interval = messages[i]['date'] - messages[i-1]['date']
            time_intervals.append(interval)
        
        # Check for regular intervals (bot behavior)
        if time_intervals:
            avg_interval = sum(time_intervals) / len(time_intervals)
            interval_variance = sum((x - avg_interval) ** 2 for x in time_intervals) / len(time_intervals)
            
            # Low variance suggests automated posting
            regularity_score = 1.0 / (1.0 + interval_variance / 100)
        else:
            regularity_score = 0.0
        
        # Check for repetitive content
        texts = [msg.get('text', '') for msg in messages]
        unique_texts = set(texts)
        repetition_score = 1.0 - (len(unique_texts) / len(texts))
        
        # Combined bot detection score
        bot_confidence = (regularity_score * 0.6) + (repetition_score * 0.4)
        
        return {
            "bot_detected": bot_confidence > 0.7,
            "confidence": bot_confidence,
            "analysis": {
                "regularity_score": regularity_score,
                "repetition_score": repetition_score,
                "avg_interval_seconds": avg_interval if time_intervals else 0,
                "message_count": len(messages)
            }
        }
    
    def _get_chat_info(self, chat_id: str) -> Optional[Dict]:
        """Get information about a chat/channel"""
        try:
            self.rate_limiter.wait_if_needed()
            
            response = self.session.get(
                f"{self.base_url}/getChat",
                params={"chat_id": chat_id}
            )
            response.raise_for_status()
            
            return response.json().get('result')
            
        except Exception as e:
            logger.error(f"Failed to get chat info for {chat_id}: {str(e)}")
            return None
    
    def _process_telegram_message(self, message: Dict) -> StandardizedPost:
        """Process Telegram message into standardized format"""
        text = message.get('text', '')
        
        # Extract hashtags and mentions
        hashtags = re.findall(r'#(\w+)', text)
        mentions = re.findall(r'@(\w+)', text)
        
        # Extract media URLs
        media_urls = []
        if message.get('photo'):
            media_urls.append('photo_attached')
        if message.get('video'):
            media_urls.append('video_attached')
        if message.get('document'):
            media_urls.append('document_attached')
        
        from_user = message.get('from', {})
        
        return StandardizedPost(
            id=str(message.get('message_id', '')),
            platform="telegram",
            content=text,
            author=from_user.get('username', from_user.get('first_name', 'unknown')),
            author_id=str(from_user.get('id', '')),
            timestamp=datetime.fromtimestamp(message.get('date', 0)),
            url=f"t.me/{message.get('chat', {}).get('username', 'unknown')}/{message.get('message_id', '')}",
            engagement={'views': message.get('views', 0), 'total': message.get('views', 0)},
            hashtags=hashtags,
            mentions=mentions,
            media_urls=media_urls,
            verified_author=from_user.get('is_verified', False),
            metadata={
                'message_id': message.get('message_id'),
                'chat': message.get('chat', {}),
                'forward_from': message.get('forward_from', {})
            }
        )

class NewsAPIManager(BaseAPIManager):
    """News API Manager for police monitoring"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, rate_limit_calls=1000, rate_limit_window=86400)  # 1000 requests per day
        self.base_url = "https://newsapi.org/v2"
        self.session.headers.update({
            "X-API-Key": api_key
        })
    
    def search_content(self, keywords: List[str], max_results: int = 100, **kwargs) -> APIResponse:
        """Search news articles by keywords"""
        try:
            self.rate_limiter.wait_if_needed()
            
            # Build search query
            query = " OR ".join([f'"{keyword}"' for keyword in keywords])
            
            params = {
                "q": query,
                "pageSize": min(max_results, 100),
                "sortBy": kwargs.get('sort_by', 'publishedAt'),
                "language": kwargs.get('language', 'en')
            }
            
            if kwargs.get('from_date'):
                params['from'] = kwargs['from_date'].isoformat()
            if kwargs.get('to_date'):
                params['to'] = kwargs['to_date'].isoformat()
            if kwargs.get('sources'):
                params['sources'] = ','.join(kwargs['sources'])
            
            response = self.session.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_news_response(data)
            
            return APIResponse(
                success=True,
                data=posts,
                total_results=data.get('totalResults', 0)
            )
            
        except requests.RequestException as e:
            logger.error(f"News API error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def get_user_content(self, user_id: str, **kwargs) -> APIResponse:
        """Not applicable for News API"""
        return APIResponse(
            success=False,
            data=[],
            error_message="User content not applicable for News API"
        )
    
    def get_top_headlines(self, **kwargs) -> APIResponse:
        """Get top headlines"""
        try:
            self.rate_limiter.wait_if_needed()
            
            params = {
                "pageSize": kwargs.get('max_results', 20),
                "country": kwargs.get('country', 'us'),
                "category": kwargs.get('category', 'general')
            }
            
            if kwargs.get('sources'):
                params['sources'] = ','.join(kwargs['sources'])
                params.pop('country', None)  # Can't use both country and sources
            
            response = self.session.get(f"{self.base_url}/top-headlines", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_news_response(data)
            
            return APIResponse(
                success=True,
                data=posts,
                total_results=data.get('totalResults', 0)
            )
            
        except requests.RequestException as e:
            logger.error(f"News API headlines error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def monitor_sources(self, sources: List[str], **kwargs) -> APIResponse:
        """Monitor specific news sources"""
        try:
            self.rate_limiter.wait_if_needed()
            
            params = {
                "sources": ",".join(sources),
                "pageSize": kwargs.get('max_results', 50),
                "sortBy": "publishedAt"
            }
            
            if kwargs.get('from_date'):
                params['from'] = kwargs['from_date'].isoformat()
            
            response = self.session.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            posts = self._process_news_response(data)
            
            return APIResponse(
                success=True,
                data=posts,
                total_results=data.get('totalResults', 0)
            )
            
        except requests.RequestException as e:
            logger.error(f"News source monitoring error: {str(e)}")
            return APIResponse(success=False, data=[], error_message=str(e))
    
    def analyze_source_reliability(self, source_id: str, articles: List[StandardizedPost]) -> Dict[str, Any]:
        """Analyze news source reliability"""
        if not articles:
            return {"error": "No articles to analyze"}
        
        # Analyze publication patterns
        publication_times = [article.timestamp for article in articles]
        publication_times.sort()
        
        # Check for regular publication schedule
        time_diffs = [(publication_times[i+1] - publication_times[i]).total_seconds() 
                     for i in range(len(publication_times)-1)]
        
        avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 0
        
        # Analyze content diversity
        unique_authors = set(article.author for article in articles)
        content_diversity = len(unique_authors) / len(articles)
        
        # Check for external links and citations
        articles_with_urls = sum(1 for article in articles if article.media_urls)
        url_ratio = articles_with_urls / len(articles)
        
        reliability_score = (content_diversity * 0.4) + (url_ratio * 0.3) + (min(1.0, avg_time_diff / 3600) * 0.3)
        
        return {
            "source_id": source_id,
            "reliability_score": reliability_score,
            "analysis": {
                "article_count": len(articles),
                "unique_authors": len(unique_authors),
                "content_diversity": content_diversity,
                "avg_publication_interval_hours": avg_time_diff / 3600,
                "articles_with_media": articles_with_urls,
                "url_ratio": url_ratio
            },
            "reliability_level": (
                "High" if reliability_score > 0.7 else
                "Medium" if reliability_score > 0.4 else
                "Low"
            )
        }
    
    def _process_news_response(self, data: Dict) -> List[StandardizedPost]:
        """Process News API response into standardized format"""
        posts = []
        
        for article in data.get('articles', []):
            # Extract potential hashtags from title and description
            title = article.get('title', '')
            description = article.get('description', '')
            content = f"{title}. {description}"
            
            hashtags = re.findall(r'#(\w+)', content)
            mentions = re.findall(r'@(\w+)', content)
            
            # Media URLs
            media_urls = []
            if article.get('urlToImage'):
                media_urls.append(article['urlToImage'])
            
            post = StandardizedPost(
                id=hashlib.md5(article.get('url', '').encode()).hexdigest()[:16],
                platform="news",
                content=content,
                author=article.get('author', article.get('source', {}).get('name', 'unknown')),
                author_id=article.get('source', {}).get('id', ''),
                timestamp=datetime.fromisoformat(article.get('publishedAt', '').replace('Z', '+00:00')),
                url=article.get('url', ''),
                engagement={'total': 0},  # News API doesn't provide engagement metrics
                hashtags=hashtags,
                mentions=mentions,
                media_urls=media_urls,
                verified_author=True,  # News sources are generally verified
                metadata={
                    'source': article.get('source', {}),
                    'title': title,
                    'description': description
                }
            )
            posts.append(post)
        
        return posts
