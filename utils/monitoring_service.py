"""
Unified Social Media API Integration Service
Coordinates multiple platform APIs for police monitoring
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from .social_media_apis import (
    TwitterAPIManager, FacebookAPIManager, TelegramAPIManager, NewsAPIManager,
    StandardizedPost, APIResponse
)

logger = logging.getLogger(__name__)

class SocialMediaMonitoringService:
    """Unified service for monitoring multiple social media platforms"""
    
    def __init__(self, api_credentials: Dict[str, str]):
        """
        Initialize with API credentials
        
        Args:
            api_credentials: Dict with keys: twitter_bearer, facebook_token, 
                           telegram_bot_token, news_api_key
        """
        self.api_managers = {}
        self.monitoring_active = False
        self.alert_callbacks = []
        
        # Initialize API managers based on available credentials
        if api_credentials.get('twitter_bearer'):
            try:
                self.api_managers['twitter'] = TwitterAPIManager(api_credentials['twitter_bearer'])
                logger.info("Twitter API manager initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Twitter API: {e}")
        
        if api_credentials.get('facebook_token'):
            try:
                self.api_managers['facebook'] = FacebookAPIManager(api_credentials['facebook_token'])
                logger.info("Facebook API manager initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Facebook API: {e}")
        
        if api_credentials.get('telegram_bot_token'):
            try:
                self.api_managers['telegram'] = TelegramAPIManager(api_credentials['telegram_bot_token'])
                logger.info("Telegram API manager initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Telegram API: {e}")
        
        if api_credentials.get('news_api_key'):
            try:
                self.api_managers['news'] = NewsAPIManager(api_credentials['news_api_key'])
                logger.info("News API manager initialized")
            except Exception as e:
                logger.error(f"Failed to initialize News API: {e}")
    
    def search_across_platforms(self, 
                               keywords: List[str], 
                               platforms: Optional[List[str]] = None,
                               max_results_per_platform: int = 50,
                               time_range: Optional[Tuple[datetime, datetime]] = None) -> Dict[str, APIResponse]:
        """
        Search for keywords across multiple platforms simultaneously
        
        Args:
            keywords: List of keywords to search for
            platforms: List of platforms to search (default: all available)
            max_results_per_platform: Maximum results per platform
            time_range: Optional tuple of (start_time, end_time)
        
        Returns:
            Dictionary mapping platform names to API responses
        """
        if platforms is None:
            platforms = list(self.api_managers.keys())
        
        results = {}
        
        # Use ThreadPoolExecutor for concurrent API calls
        with ThreadPoolExecutor(max_workers=len(platforms)) as executor:
            future_to_platform = {}
            
            for platform in platforms:
                if platform in self.api_managers:
                    manager = self.api_managers[platform]
                    
                    # Prepare kwargs for the search
                    kwargs = {'max_results': max_results_per_platform}
                    if time_range:
                        kwargs['start_time'] = time_range[0]
                        kwargs['end_time'] = time_range[1]
                    
                    # Submit the search task
                    future = executor.submit(manager.search_content, keywords, **kwargs)
                    future_to_platform[future] = platform
            
            # Collect results as they complete
            for future in as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    response = future.result(timeout=30)  # 30 second timeout
                    results[platform] = response
                    logger.info(f"Completed search for {platform}: {len(response.data)} posts")
                except Exception as e:
                    logger.error(f"Search failed for {platform}: {e}")
                    results[platform] = APIResponse(
                        success=False, 
                        data=[], 
                        error_message=str(e)
                    )
        
        return results
    
    def monitor_users_across_platforms(self, 
                                     user_targets: Dict[str, List[str]],
                                     max_results_per_user: int = 100) -> Dict[str, Dict[str, APIResponse]]:
        """
        Monitor specific users across platforms
        
        Args:
            user_targets: Dict mapping platform names to lists of user IDs
            max_results_per_user: Maximum results per user
        
        Returns:
            Nested dict: {platform: {user_id: APIResponse}}
        """
        results = {}
        
        for platform, user_ids in user_targets.items():
            if platform not in self.api_managers:
                logger.warning(f"Platform {platform} not available")
                continue
            
            manager = self.api_managers[platform]
            platform_results = {}
            
            for user_id in user_ids:
                try:
                    response = manager.get_user_content(user_id, max_results=max_results_per_user)
                    platform_results[user_id] = response
                    logger.info(f"Monitored {platform} user {user_id}: {len(response.data)} posts")
                except Exception as e:
                    logger.error(f"Failed to monitor {platform} user {user_id}: {e}")
                    platform_results[user_id] = APIResponse(
                        success=False,
                        data=[],
                        error_message=str(e)
                    )
            
            results[platform] = platform_results
        
        return results
    
    def detect_threats_and_campaigns(self, posts: List[StandardizedPost]) -> Dict[str, Any]:
        """
        Analyze posts for potential threats and coordinated campaigns
        
        Args:
            posts: List of standardized posts to analyze
        
        Returns:
            Threat analysis results
        """
        if not posts:
            return {"threats_detected": False, "campaigns_detected": False}
        
        threat_analysis = {
            "total_posts_analyzed": len(posts),
            "threats_detected": False,
            "campaigns_detected": False,
            "high_risk_posts": [],
            "campaign_indicators": {},
            "threat_keywords": [],
            "suspicious_patterns": []
        }
        
        # Define threat keywords (can be expanded)
        threat_keywords = [
            'bomb', 'attack', 'terror', 'kill', 'weapon', 'explosive',
            'violence', 'threat', 'harm', 'protest', 'riot', 'demonstration'
        ]
        
        # Analyze individual posts for threats
        high_risk_posts = []
        for post in posts:
            risk_score = 0
            detected_keywords = []
            
            content_lower = post.content.lower()
            
            # Check for threat keywords
            for keyword in threat_keywords:
                if keyword in content_lower:
                    risk_score += 2
                    detected_keywords.append(keyword)
            
            # Check for urgency indicators
            urgency_indicators = ['now', 'today', 'tonight', 'urgent', 'asap', 'immediately']
            for indicator in urgency_indicators:
                if indicator in content_lower:
                    risk_score += 1
            
            # Check for location mentions
            if post.location or any(word in content_lower for word in ['address', 'location', 'place', 'building']):
                risk_score += 1
            
            # Check engagement patterns (high engagement on threatening content)
            if post.engagement.get('total', 0) > 100 and detected_keywords:
                risk_score += 2
            
            if risk_score >= 3:
                post.threat_level = "high" if risk_score >= 5 else "medium"
                high_risk_posts.append({
                    "post": post,
                    "risk_score": risk_score,
                    "detected_keywords": detected_keywords
                })
        
        if high_risk_posts:
            threat_analysis["threats_detected"] = True
            threat_analysis["high_risk_posts"] = high_risk_posts
            threat_analysis["threat_keywords"] = list(set(
                keyword for post_data in high_risk_posts 
                for keyword in post_data["detected_keywords"]
            ))
        
        # Campaign detection across platforms
        campaign_analysis = self._detect_cross_platform_campaigns(posts)
        if campaign_analysis["suspicious"]:
            threat_analysis["campaigns_detected"] = True
            threat_analysis["campaign_indicators"] = campaign_analysis
        
        return threat_analysis
    
    def generate_intelligence_report(self, 
                                   search_results: Dict[str, APIResponse],
                                   time_period: str = "last_24_hours") -> Dict[str, Any]:
        """
        Generate comprehensive intelligence report from search results
        
        Args:
            search_results: Results from search_across_platforms
            time_period: Description of time period analyzed
        
        Returns:
            Intelligence report
        """
        all_posts = []
        platform_stats = {}
        
        # Collect all posts and platform statistics
        for platform, response in search_results.items():
            platform_stats[platform] = {
                "success": response.success,
                "posts_collected": len(response.data),
                "error": response.error_message
            }
            
            if response.success:
                all_posts.extend(response.data)
        
        # Threat analysis
        threat_analysis = self.detect_threats_and_campaigns(all_posts)
        
        # Engagement analysis
        engagement_stats = self._analyze_engagement_patterns(all_posts)
        
        # Temporal analysis
        temporal_analysis = self._analyze_temporal_patterns(all_posts)
        
        # Geographic analysis
        geographic_analysis = self._analyze_geographic_patterns(all_posts)
        
        # Generate summary
        report = {
            "report_generated": datetime.now().isoformat(),
            "time_period": time_period,
            "summary": {
                "total_posts_analyzed": len(all_posts),
                "platforms_monitored": len([p for p, s in platform_stats.items() if s["success"]]),
                "threats_detected": threat_analysis["threats_detected"],
                "campaigns_detected": threat_analysis["campaigns_detected"],
                "high_risk_posts_count": len(threat_analysis["high_risk_posts"])
            },
            "platform_statistics": platform_stats,
            "threat_analysis": threat_analysis,
            "engagement_analysis": engagement_stats,
            "temporal_analysis": temporal_analysis,
            "geographic_analysis": geographic_analysis,
            "recommendations": self._generate_recommendations(threat_analysis, all_posts)
        }
        
        return report
    
    def setup_real_time_monitoring(self, 
                                 keywords: List[str],
                                 check_interval_minutes: int = 15,
                                 alert_threshold: str = "medium") -> bool:
        """
        Setup real-time monitoring with periodic checks
        
        Args:
            keywords: Keywords to monitor
            check_interval_minutes: How often to check for new content
            alert_threshold: Minimum threat level for alerts (low, medium, high)
        
        Returns:
            True if monitoring setup successful
        """
        try:
            self.monitoring_keywords = keywords
            self.check_interval = check_interval_minutes * 60  # Convert to seconds
            self.alert_threshold = alert_threshold
            self.monitoring_active = True
            
            logger.info(f"Real-time monitoring setup for keywords: {keywords}")
            logger.info(f"Check interval: {check_interval_minutes} minutes")
            logger.info(f"Alert threshold: {alert_threshold}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup real-time monitoring: {e}")
            return False
    
    def add_alert_callback(self, callback_function):
        """Add callback function for real-time alerts"""
        self.alert_callbacks.append(callback_function)
    
    def get_platform_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all configured platforms"""
        status = {}
        
        for platform, manager in self.api_managers.items():
            try:
                # Test basic connectivity
                if platform == 'twitter':
                    # Try a simple search with rate limit check
                    test_response = manager.search_content(['test'], max_results=1)
                elif platform == 'facebook':
                    # Facebook has limited search, check differently
                    test_response = APIResponse(success=True, data=[])
                elif platform == 'telegram':
                    # Check bot info
                    bot_info = manager.get_bot_info()
                    test_response = APIResponse(success=bool(bot_info), data=[])
                elif platform == 'news':
                    # Try headlines
                    test_response = manager.get_top_headlines(max_results=1)
                else:
                    test_response = APIResponse(success=False, data=[])
                
                status[platform] = {
                    "available": True,
                    "connected": test_response.success,
                    "rate_limit_remaining": test_response.rate_limit_remaining,
                    "last_checked": datetime.now().isoformat(),
                    "error": test_response.error_message
                }
                
            except Exception as e:
                status[platform] = {
                    "available": True,
                    "connected": False,
                    "error": str(e),
                    "last_checked": datetime.now().isoformat()
                }
        
        return status
    
    def _detect_cross_platform_campaigns(self, posts: List[StandardizedPost]) -> Dict[str, Any]:
        """Detect coordinated campaigns across multiple platforms"""
        if len(posts) < 5:
            return {"suspicious": False, "confidence": 0.0}
        
        # Group posts by platform
        platform_posts = {}
        for post in posts:
            if post.platform not in platform_posts:
                platform_posts[post.platform] = []
            platform_posts[post.platform].append(post)
        
        # Only analyze if we have posts from multiple platforms
        if len(platform_posts) < 2:
            return {"suspicious": False, "confidence": 0.0}
        
        # Analyze content similarity across platforms
        all_content = [post.content.lower() for post in posts]
        unique_content = set(all_content)
        similarity_ratio = 1 - (len(unique_content) / len(all_content))
        
        # Analyze hashtag coordination
        all_hashtags = []
        for post in posts:
            all_hashtags.extend([tag.lower() for tag in post.hashtags])
        
        hashtag_frequency = {}
        for tag in all_hashtags:
            hashtag_frequency[tag] = hashtag_frequency.get(tag, 0) + 1
        
        # Check for coordinated hashtag usage
        coordinated_hashtags = [tag for tag, freq in hashtag_frequency.items() 
                              if freq >= len(platform_posts) and freq > 2]
        
        # Temporal coordination analysis
        timestamps = [post.timestamp for post in posts]
        timestamps.sort()
        
        # Calculate time clustering
        time_clusters = 0
        cluster_threshold = timedelta(hours=1)
        
        for i in range(len(timestamps) - 1):
            if timestamps[i+1] - timestamps[i] <= cluster_threshold:
                time_clusters += 1
        
        temporal_coordination = time_clusters / max(len(timestamps) - 1, 1)
        
        # Calculate overall suspicion score
        confidence = (
            similarity_ratio * 0.4 +
            (len(coordinated_hashtags) / max(len(set(all_hashtags)), 1)) * 0.3 +
            temporal_coordination * 0.3
        )
        
        return {
            "suspicious": confidence > 0.6,
            "confidence": confidence,
            "platforms_involved": list(platform_posts.keys()),
            "content_similarity": similarity_ratio,
            "coordinated_hashtags": coordinated_hashtags,
            "temporal_coordination": temporal_coordination,
            "analysis_details": {
                "total_posts": len(posts),
                "unique_content_ratio": len(unique_content) / len(all_content),
                "hashtag_overlap": len(coordinated_hashtags),
                "time_clusters": time_clusters
            }
        }
    
    def _analyze_engagement_patterns(self, posts: List[StandardizedPost]) -> Dict[str, Any]:
        """Analyze engagement patterns across posts"""
        if not posts:
            return {}
        
        total_engagement = sum(post.engagement.get('total', 0) for post in posts)
        avg_engagement = total_engagement / len(posts)
        
        # Platform breakdown
        platform_engagement = {}
        for post in posts:
            platform = post.platform
            if platform not in platform_engagement:
                platform_engagement[platform] = []
            platform_engagement[platform].append(post.engagement.get('total', 0))
        
        # Calculate platform averages
        platform_averages = {}
        for platform, engagements in platform_engagement.items():
            platform_averages[platform] = sum(engagements) / len(engagements)
        
        return {
            "total_engagement": total_engagement,
            "average_engagement": avg_engagement,
            "platform_breakdown": platform_averages,
            "high_engagement_posts": [
                post for post in posts 
                if post.engagement.get('total', 0) > avg_engagement * 2
            ]
        }
    
    def _analyze_temporal_patterns(self, posts: List[StandardizedPost]) -> Dict[str, Any]:
        """Analyze temporal posting patterns"""
        if not posts:
            return {}
        
        timestamps = [post.timestamp for post in posts]
        timestamps.sort()
        
        # Hour distribution
        hour_distribution = {}
        for timestamp in timestamps:
            hour = timestamp.hour
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
        
        # Day of week distribution
        weekday_distribution = {}
        for timestamp in timestamps:
            weekday = timestamp.strftime('%A')
            weekday_distribution[weekday] = weekday_distribution.get(weekday, 0) + 1
        
        # Peak posting times
        peak_hour = max(hour_distribution, key=hour_distribution.get) if hour_distribution else None
        peak_day = max(weekday_distribution, key=weekday_distribution.get) if weekday_distribution else None
        
        return {
            "total_posts": len(posts),
            "time_range": {
                "start": timestamps[0].isoformat() if timestamps else None,
                "end": timestamps[-1].isoformat() if timestamps else None
            },
            "hour_distribution": hour_distribution,
            "weekday_distribution": weekday_distribution,
            "peak_posting_hour": peak_hour,
            "peak_posting_day": peak_day
        }
    
    def _analyze_geographic_patterns(self, posts: List[StandardizedPost]) -> Dict[str, Any]:
        """Analyze geographic patterns in posts"""
        locations = [post.location for post in posts if post.location]
        
        if not locations:
            return {"geographic_data": "insufficient"}
        
        location_frequency = {}
        for location in locations:
            location_frequency[location] = location_frequency.get(location, 0) + 1
        
        # Top locations
        top_locations = sorted(location_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "posts_with_location": len(locations),
            "total_posts": len(posts),
            "location_coverage": len(locations) / len(posts),
            "unique_locations": len(set(locations)),
            "top_locations": top_locations,
            "geographic_spread": len(set(locations)) / len(locations) if locations else 0
        }
    
    def _generate_recommendations(self, threat_analysis: Dict[str, Any], posts: List[StandardizedPost]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        if threat_analysis["threats_detected"]:
            recommendations.append("IMMEDIATE: High-risk content detected. Review flagged posts for potential threats.")
            recommendations.append("Contact relevant authorities if credible threats are identified.")
        
        if threat_analysis["campaigns_detected"]:
            recommendations.append("ALERT: Potential coordinated campaign detected across platforms.")
            recommendations.append("Investigate user accounts involved in coordinated messaging.")
        
        if len(posts) > 1000:
            recommendations.append("HIGH VOLUME: Large number of posts detected. Consider narrowing search criteria.")
        
        # Platform-specific recommendations
        platforms = set(post.platform for post in posts)
        if 'twitter' in platforms and 'facebook' in platforms:
            recommendations.append("Cross-platform activity detected. Monitor for message consistency.")
        
        if not recommendations:
            recommendations.append("No immediate threats detected. Continue routine monitoring.")
        
        return recommendations
