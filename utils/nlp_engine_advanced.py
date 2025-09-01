"""
Advanced NLP Engine Functions - Part 2
Contains coordination detection, threat classification, and other advanced functions
"""

import numpy as np
import re
from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

class AdvancedNLPFunctions:
    """Additional advanced functions for the NLP engine"""
    
    def __init__(self, main_engine):
        self.main_engine = main_engine
    
    def detect_coordination(self, posts: List[Dict[str, Any]], 
                          advanced_analysis: bool = True) -> 'CoordinationResult':
        """
        Advanced coordination detection with sophisticated pattern analysis
        
        Args:
            posts: List of posts with content and metadata
            advanced_analysis: Whether to perform advanced ML-based analysis
            
        Returns:
            Enhanced CoordinationResult with detailed coordination analysis
        """
        try:
            if len(posts) < 2:
                return self._create_empty_coordination_result()
            
            coordination_indicators = []
            similar_patterns = []
            similarity_scores = []
            campaign_indicators = {}
            temporal_coordination = {}
            content_coordination = {}
            behavioral_coordination = {}
            
            # 1. Advanced Content Similarity Analysis
            content_results = self._analyze_content_coordination(posts)
            content_coordination = content_results
            similarity_scores.extend(content_results['similarity_scores'])
            similar_patterns.extend(content_results['patterns'])
            coordination_indicators.extend(content_results['indicators'])
            
            # 2. Temporal Coordination Analysis
            temporal_results = self._analyze_temporal_coordination(posts)
            temporal_coordination = temporal_results
            coordination_indicators.extend(temporal_results['indicators'])
            
            # 3. Behavioral Coordination Analysis
            behavioral_results = self._analyze_behavioral_coordination(posts)
            behavioral_coordination = behavioral_results
            coordination_indicators.extend(behavioral_results['indicators'])
            
            # 4. Network-based Coordination
            if advanced_analysis:
                network_results = self._analyze_network_coordination(posts)
                coordination_indicators.extend(network_results['indicators'])
                campaign_indicators.update(network_results['campaign_indicators'])
            
            # 5. Hashtag and URL Coordination
            hashtag_results = self._analyze_hashtag_coordination(posts)
            coordination_indicators.extend(hashtag_results['indicators'])
            
            # 6. Language and Style Coordination
            style_results = self._analyze_style_coordination(posts)
            coordination_indicators.extend(style_results['indicators'])
            
            # Calculate overall coordination scores
            coordination_metrics = self._calculate_coordination_metrics(
                content_coordination, temporal_coordination, 
                behavioral_coordination, len(posts)
            )
            
            # Determine coordination type and sophistication
            coordination_type = self._determine_coordination_type(
                content_coordination, temporal_coordination, behavioral_coordination
            )
            
            coordination_sophistication = self._assess_coordination_sophistication(
                coordination_indicators, similarity_scores
            )
            
            # Estimate network size
            network_size_estimate = self._estimate_network_size(posts, coordination_indicators)
            
            # Final coordination assessment
            overall_similarity = coordination_metrics['overall_score']
            is_coordinated = overall_similarity > 0.6
            confidence = min(0.95, coordination_metrics['confidence'])
            
            from utils.nlp_engine import CoordinationResult
            return CoordinationResult(
                similarity_score=overall_similarity,
                is_coordinated=is_coordinated,
                confidence=confidence,
                similar_patterns=similar_patterns,
                coordination_indicators=coordination_indicators,
                coordination_type=coordination_type,
                network_size_estimate=network_size_estimate,
                coordination_sophistication=coordination_sophistication,
                campaign_indicators=campaign_indicators,
                temporal_coordination=temporal_coordination,
                content_coordination=content_coordination,
                behavioral_coordination=behavioral_coordination
            )
            
        except Exception as e:
            logger.error(f"Coordination detection error: {str(e)}")
            return self._create_empty_coordination_result()
    
    def _analyze_content_coordination(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content-based coordination patterns"""
        results = {
            'similarity_scores': [],
            'patterns': [],
            'indicators': [],
            'content_clusters': [],
            'template_usage': 0.0
        }
        
        try:
            contents = [post.get('content', '') for post in posts]
            
            # Content similarity matrix
            similarity_matrix = []
            for i in range(len(contents)):
                row = []
                for j in range(len(contents)):
                    if i != j:
                        similarity = self._calculate_advanced_similarity(contents[i], contents[j])
                        row.append(similarity)
                        results['similarity_scores'].append(similarity)
                    else:
                        row.append(1.0)
                similarity_matrix.append(row)
            
            # Detect high similarity clusters
            high_similarity_pairs = []
            for i in range(len(similarity_matrix)):
                for j in range(i + 1, len(similarity_matrix[i])):
                    if similarity_matrix[i][j] > 0.8:
                        high_similarity_pairs.append((i, j, similarity_matrix[i][j]))
                        results['patterns'].append(
                            f"High content similarity between posts {i+1} and {j+1} ({similarity_matrix[i][j]:.2f})"
                        )
            
            # Template detection
            if len(contents) > 2:
                template_score = self._detect_content_templates(contents)
                results['template_usage'] = template_score
                
                if template_score > 0.7:
                    results['indicators'].append("Template-based content coordination detected")
                elif template_score > 0.5:
                    results['indicators'].append("Potential template usage detected")
            
            # URL and link coordination
            url_coordination = self._analyze_url_coordination(contents)
            if url_coordination['coordinated']:
                results['indicators'].extend(url_coordination['indicators'])
            
        except Exception as e:
            logger.debug(f"Content coordination analysis error: {e}")
        
        return results
    
    def _analyze_temporal_coordination(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal coordination patterns"""
        results = {
            'indicators': [],
            'time_clusters': [],
            'posting_intervals': [],
            'synchronized_posting': False,
            'regular_intervals': False
        }
        
        try:
            timestamps = []
            for post in posts:
                timestamp = post.get('timestamp')
                if timestamp:
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        except:
                            continue
                    timestamps.append(timestamp)
            
            if len(timestamps) < 2:
                return results
            
            # Sort timestamps
            timestamps.sort()
            
            # Calculate intervals
            intervals = []
            for i in range(len(timestamps) - 1):
                interval = (timestamps[i + 1] - timestamps[i]).total_seconds()
                intervals.append(interval)
                results['posting_intervals'].append(interval)
            
            if intervals:
                # Check for synchronized posting (posts within short time windows)
                short_intervals = [i for i in intervals if i < 300]  # 5 minutes
                if len(short_intervals) > len(intervals) * 0.5:
                    results['synchronized_posting'] = True
                    results['indicators'].append("Synchronized posting detected (multiple posts within 5 minutes)")
                
                # Check for regular intervals
                if len(intervals) > 3:
                    mean_interval = np.mean(intervals)
                    std_interval = np.std(intervals)
                    cv = std_interval / mean_interval if mean_interval > 0 else float('inf')
                    
                    if cv < 0.3:  # Low coefficient of variation
                        results['regular_intervals'] = True
                        results['indicators'].append(f"Regular posting intervals detected (CV: {cv:.2f})")
                
                # Detect burst patterns
                burst_threshold = np.mean(intervals) - 2 * np.std(intervals)
                burst_count = sum(1 for i in intervals if i < burst_threshold and i > 0)
                
                if burst_count > len(intervals) * 0.3:
                    results['indicators'].append("Burst posting patterns detected")
            
        except Exception as e:
            logger.debug(f"Temporal coordination analysis error: {e}")
        
        return results
    
    def _analyze_behavioral_coordination(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze behavioral coordination patterns"""
        results = {
            'indicators': [],
            'user_similarities': [],
            'engagement_patterns': {},
            'activity_correlation': 0.0
        }
        
        try:
            # Extract user metadata
            user_data = []
            for post in posts:
                metadata = post.get('metadata', {})
                user_info = {
                    'user_id': post.get('user_id', ''),
                    'followers': metadata.get('followers', 0),
                    'following': metadata.get('following', 0),
                    'account_age': metadata.get('account_age_days', 365),
                    'verified': metadata.get('verified', False)
                }
                user_data.append(user_info)
            
            if len(user_data) > 1:
                # Analyze user similarity
                similarities = self._calculate_user_similarities(user_data)
                results['user_similarities'] = similarities
                
                if similarities['avg_similarity'] > 0.8:
                    results['indicators'].append("High user profile similarity detected")
                
                # Account age clustering
                ages = [u['account_age'] for u in user_data if u['account_age'] > 0]
                if len(ages) > 2:
                    age_std = np.std(ages)
                    age_mean = np.mean(ages)
                    if age_std < age_mean * 0.2:
                        results['indicators'].append("Similar account creation times detected")
                
                # Follower pattern analysis
                follower_counts = [u['followers'] for u in user_data]
                if len(follower_counts) > 2:
                    follower_cv = np.std(follower_counts) / np.mean(follower_counts) if np.mean(follower_counts) > 0 else 0
                    if follower_cv < 0.3:
                        results['indicators'].append("Similar follower counts across accounts")
            
        except Exception as e:
            logger.debug(f"Behavioral coordination analysis error: {e}")
        
        return results
    
    def _analyze_network_coordination(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze network-level coordination indicators"""
        results = {
            'indicators': [],
            'campaign_indicators': {},
            'network_density': 0.0
        }
        
        try:
            # Extract network indicators
            user_ids = [post.get('user_id', '') for post in posts]
            unique_users = set(user_ids)
            
            # Calculate network metrics
            if len(unique_users) > 1:
                # Network density (simplified)
                total_possible_connections = len(unique_users) * (len(unique_users) - 1)
                # In a real implementation, this would analyze actual follower networks
                estimated_connections = len(posts)  # Simplified estimate
                
                results['network_density'] = estimated_connections / total_possible_connections if total_possible_connections > 0 else 0
                
                if results['network_density'] > 0.7:
                    results['indicators'].append("High network density detected")
            
            # Campaign indicators
            hashtags = []
            mentions = []
            for post in posts:
                content = post.get('content', '')
                hashtags.extend(re.findall(r'#(\w+)', content.lower()))
                mentions.extend(re.findall(r'@(\w+)', content.lower()))
            
            # Common campaign hashtags
            hashtag_counts = Counter(hashtags)
            common_hashtags = [tag for tag, count in hashtag_counts.items() if count > len(posts) * 0.5]
            
            if common_hashtags:
                results['campaign_indicators']['common_hashtags'] = common_hashtags
                results['indicators'].append(f"Campaign hashtags detected: {', '.join(common_hashtags[:3])}")
            
            # Coordinated mentions
            mention_counts = Counter(mentions)
            coordinated_mentions = [mention for mention, count in mention_counts.items() if count > len(posts) * 0.3]
            
            if coordinated_mentions:
                results['campaign_indicators']['coordinated_mentions'] = coordinated_mentions
                results['indicators'].append("Coordinated mention patterns detected")
            
        except Exception as e:
            logger.debug(f"Network coordination analysis error: {e}")
        
        return results
    
    def _analyze_hashtag_coordination(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze hashtag coordination patterns"""
        results = {'indicators': []}
        
        try:
            all_hashtags = []
            post_hashtags = []
            
            for post in posts:
                content = post.get('content', '')
                hashtags = re.findall(r'#(\w+)', content.lower())
                post_hashtags.append(set(hashtags))
                all_hashtags.extend(hashtags)
            
            if all_hashtags:
                hashtag_counts = Counter(all_hashtags)
                
                # Find hashtags used by multiple posts
                coordinated_hashtags = {tag: count for tag, count in hashtag_counts.items() 
                                      if count > 1 and count >= len(posts) * 0.3}
                
                if coordinated_hashtags:
                    results['indicators'].append(
                        f"Coordinated hashtag usage: {', '.join(list(coordinated_hashtags.keys())[:3])}"
                    )
                
                # Check for hashtag sequence similarity
                if len(post_hashtags) > 2:
                    similarities = []
                    for i in range(len(post_hashtags)):
                        for j in range(i + 1, len(post_hashtags)):
                            if post_hashtags[i] and post_hashtags[j]:
                                jaccard = len(post_hashtags[i] & post_hashtags[j]) / len(post_hashtags[i] | post_hashtags[j])
                                similarities.append(jaccard)
                    
                    if similarities and np.mean(similarities) > 0.6:
                        results['indicators'].append("High hashtag similarity between posts")
        
        except Exception as e:
            logger.debug(f"Hashtag coordination analysis error: {e}")
        
        return results
    
    def _analyze_style_coordination(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze writing style coordination"""
        results = {'indicators': []}
        
        try:
            contents = [post.get('content', '') for post in posts if post.get('content')]
            
            if len(contents) < 2:
                return results
            
            # Analyze linguistic features
            features = []
            for content in contents:
                feature_vector = {
                    'avg_word_length': np.mean([len(word) for word in content.split()]) if content.split() else 0,
                    'avg_sentence_length': len(content.split()) / max(1, len(re.split(r'[.!?]+', content))),
                    'punctuation_ratio': len(re.findall(r'[.!?,:;]', content)) / len(content) if content else 0,
                    'caps_ratio': len(re.findall(r'[A-Z]', content)) / len(content) if content else 0,
                    'question_ratio': content.count('?') / len(content) if content else 0,
                    'exclamation_ratio': content.count('!') / len(content) if content else 0
                }
                features.append(feature_vector)
            
            # Calculate style similarity
            if len(features) > 1:
                style_similarities = []
                for feature_name in features[0].keys():
                    values = [f[feature_name] for f in features]
                    if values and np.std(values) < np.mean(values) * 0.3:  # Low variation
                        style_similarities.append(feature_name)
                
                if len(style_similarities) > 3:
                    results['indicators'].append("Consistent writing style patterns detected")
        
        except Exception as e:
            logger.debug(f"Style coordination analysis error: {e}")
        
        return results
    
    def _calculate_advanced_similarity(self, text1: str, text2: str) -> float:
        """Calculate advanced similarity between texts"""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Word-level similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            jaccard = len(words1 & words2) / len(words1 | words2)
            
            # Character n-gram similarity
            def get_ngrams(text, n=3):
                return set(text[i:i+n] for i in range(len(text)-n+1))
            
            ngrams1 = get_ngrams(text1.lower())
            ngrams2 = get_ngrams(text2.lower())
            
            ngram_similarity = 0.0
            if ngrams1 and ngrams2:
                ngram_similarity = len(ngrams1 & ngrams2) / len(ngrams1 | ngrams2)
            
            # Combine similarities
            combined_similarity = (jaccard * 0.7) + (ngram_similarity * 0.3)
            
            return combined_similarity
            
        except Exception:
            return 0.0
    
    def _detect_content_templates(self, contents: List[str]) -> float:
        """Detect template-based content generation"""
        try:
            if len(contents) < 3:
                return 0.0
            
            # Analyze structure patterns
            structures = []
            for content in contents:
                structure = {
                    'has_url': bool(re.search(r'http[s]?://\S+', content)),
                    'has_hashtag': bool(re.search(r'#\w+', content)),
                    'has_mention': bool(re.search(r'@\w+', content)),
                    'word_count_bucket': len(content.split()) // 10,  # Bucket by 10s
                    'starts_with_caps': content.strip().startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) if content.strip() else False
                }
                structures.append(structure)
            
            # Calculate structure consistency
            consistency_scores = []
            for key in structures[0].keys():
                values = [s[key] for s in structures]
                if isinstance(values[0], bool):
                    consistency = len(set(values)) == 1
                    consistency_scores.append(1.0 if consistency else 0.0)
                else:
                    # For numeric values, check variance
                    if len(set(values)) <= 2:  # Very low variation
                        consistency_scores.append(0.8)
                    else:
                        consistency_scores.append(0.0)
            
            return np.mean(consistency_scores)
            
        except Exception:
            return 0.0
    
    def _analyze_url_coordination(self, contents: List[str]) -> Dict[str, Any]:
        """Analyze URL sharing coordination"""
        results = {'coordinated': False, 'indicators': []}
        
        try:
            all_urls = []
            for content in contents:
                urls = re.findall(r'http[s]?://\S+', content)
                all_urls.extend(urls)
            
            if all_urls:
                url_counts = Counter(all_urls)
                shared_urls = [url for url, count in url_counts.items() if count > 1]
                
                if shared_urls:
                    results['coordinated'] = True
                    results['indicators'].append(f"Shared URLs detected: {len(shared_urls)} unique URLs")
                
                # Check for URL pattern similarity (same domain, etc.)
                domains = []
                for url in all_urls:
                    try:
                        domain = re.search(r'https?://([^/]+)', url)
                        if domain:
                            domains.append(domain.group(1))
                    except:
                        continue
                
                if domains:
                    domain_counts = Counter(domains)
                    dominant_domains = [domain for domain, count in domain_counts.items() 
                                     if count > len(contents) * 0.5]
                    
                    if dominant_domains:
                        results['indicators'].append(f"Coordinated domain usage: {', '.join(dominant_domains)}")
        
        except Exception as e:
            logger.debug(f"URL coordination analysis error: {e}")
        
        return results
    
    def _calculate_user_similarities(self, user_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate similarities between user profiles"""
        try:
            if len(user_data) < 2:
                return {'avg_similarity': 0.0, 'similar_pairs': []}
            
            similarities = []
            similar_pairs = []
            
            for i in range(len(user_data)):
                for j in range(i + 1, len(user_data)):
                    user1, user2 = user_data[i], user_data[j]
                    
                    # Calculate similarity score
                    similarity_score = 0.0
                    factors = 0
                    
                    # Follower count similarity
                    if user1['followers'] > 0 and user2['followers'] > 0:
                        ratio = min(user1['followers'], user2['followers']) / max(user1['followers'], user2['followers'])
                        similarity_score += ratio
                        factors += 1
                    
                    # Account age similarity
                    if user1['account_age'] > 0 and user2['account_age'] > 0:
                        age_diff = abs(user1['account_age'] - user2['account_age'])
                        age_similarity = 1 - min(age_diff / 365, 1.0)  # Normalize by year
                        similarity_score += age_similarity
                        factors += 1
                    
                    # Verification status
                    if user1['verified'] == user2['verified']:
                        similarity_score += 1.0
                        factors += 1
                    
                    if factors > 0:
                        final_similarity = similarity_score / factors
                        similarities.append(final_similarity)
                        
                        if final_similarity > 0.8:
                            similar_pairs.append((i, j, final_similarity))
            
            return {
                'avg_similarity': np.mean(similarities) if similarities else 0.0,
                'similar_pairs': similar_pairs
            }
            
        except Exception:
            return {'avg_similarity': 0.0, 'similar_pairs': []}
    
    def _calculate_coordination_metrics(self, content_coord: Dict, temporal_coord: Dict, 
                                      behavioral_coord: Dict, post_count: int) -> Dict[str, Any]:
        """Calculate overall coordination metrics"""
        try:
            # Weight different coordination types
            weights = {
                'content': 0.4,
                'temporal': 0.3,
                'behavioral': 0.3
            }
            
            # Content coordination score
            content_score = 0.0
            if content_coord.get('similarity_scores'):
                content_score = np.mean(content_coord['similarity_scores'])
            content_score += content_coord.get('template_usage', 0) * 0.3
            
            # Temporal coordination score
            temporal_score = 0.0
            if temporal_coord.get('synchronized_posting'):
                temporal_score += 0.6
            if temporal_coord.get('regular_intervals'):
                temporal_score += 0.4
            
            # Behavioral coordination score
            behavioral_score = 0.0
            if behavioral_coord.get('user_similarities'):
                behavioral_score = behavioral_coord['user_similarities'].get('avg_similarity', 0)
            
            # Overall score
            overall_score = (content_score * weights['content'] + 
                           temporal_score * weights['temporal'] + 
                           behavioral_score * weights['behavioral'])
            
            # Confidence calculation
            confidence_factors = [
                min(post_count / 5, 1.0),  # More posts = higher confidence
                len(content_coord.get('indicators', [])) * 0.1,
                len(temporal_coord.get('indicators', [])) * 0.1,
                len(behavioral_coord.get('indicators', [])) * 0.1
            ]
            
            confidence = min(0.95, sum(confidence_factors) / len(confidence_factors))
            
            return {
                'overall_score': min(1.0, overall_score),
                'content_score': min(1.0, content_score),
                'temporal_score': min(1.0, temporal_score),
                'behavioral_score': min(1.0, behavioral_score),
                'confidence': confidence
            }
            
        except Exception:
            return {
                'overall_score': 0.0,
                'content_score': 0.0,
                'temporal_score': 0.0,
                'behavioral_score': 0.0,
                'confidence': 0.0
            }
    
    def _determine_coordination_type(self, content_coord: Dict, temporal_coord: Dict, 
                                   behavioral_coord: Dict) -> str:
        """Determine the primary type of coordination"""
        try:
            scores = {
                'CONTENT': len(content_coord.get('indicators', [])),
                'TIMING': len(temporal_coord.get('indicators', [])),
                'BEHAVIORAL': len(behavioral_coord.get('indicators', [])),
                'NETWORK': 0  # Would be calculated if network data available
            }
            
            if not any(scores.values()):
                return 'NO_COORDINATION'
            
            max_type = max(scores, key=scores.get)
            
            # Check for hybrid coordination
            high_scores = [coord_type for coord_type, score in scores.items() if score >= 2]
            
            if len(high_scores) > 1:
                return 'HYBRID_COORDINATION'
            
            return max_type
            
        except Exception:
            return 'UNKNOWN'
    
    def _assess_coordination_sophistication(self, indicators: List[str], 
                                          similarities: List[float]) -> str:
        """Assess the sophistication level of coordination"""
        try:
            sophistication_score = 0
            
            # Number of coordination indicators
            sophistication_score += len(indicators)
            
            # High similarity scores indicate sophisticated coordination
            if similarities:
                avg_similarity = np.mean(similarities)
                if avg_similarity > 0.9:
                    sophistication_score += 3
                elif avg_similarity > 0.7:
                    sophistication_score += 2
                elif avg_similarity > 0.5:
                    sophistication_score += 1
            
            # Specific sophisticated patterns
            sophisticated_patterns = [
                'template', 'synchronized', 'campaign', 'coordinated'
            ]
            
            for indicator in indicators:
                if any(pattern in indicator.lower() for pattern in sophisticated_patterns):
                    sophistication_score += 1
            
            if sophistication_score >= 8:
                return 'HIGHLY_SOPHISTICATED'
            elif sophistication_score >= 5:
                return 'SOPHISTICATED'
            elif sophistication_score >= 3:
                return 'MODERATE'
            else:
                return 'BASIC'
                
        except Exception:
            return 'UNKNOWN'
    
    def _estimate_network_size(self, posts: List[Dict[str, Any]], 
                             indicators: List[str]) -> int:
        """Estimate the size of the coordinated network"""
        try:
            # Basic estimation based on unique users and coordination strength
            unique_users = len(set(post.get('user_id', '') for post in posts))
            
            # Estimate based on coordination indicators
            coordination_strength = len(indicators)
            
            if coordination_strength >= 5:
                # Strong coordination suggests larger network
                estimated_multiplier = 2.5
            elif coordination_strength >= 3:
                estimated_multiplier = 2.0
            else:
                estimated_multiplier = 1.5
            
            estimated_size = int(unique_users * estimated_multiplier)
            
            return min(estimated_size, 1000)  # Cap at reasonable maximum
            
        except Exception:
            return len(posts) if posts else 1
    
    def _create_empty_coordination_result(self):
        """Create an empty coordination result for error cases"""
        from utils.nlp_engine import CoordinationResult
        return CoordinationResult(
            similarity_score=0.0,
            is_coordinated=False,
            confidence=0.0,
            similar_patterns=[],
            coordination_indicators=[],
            coordination_type='NO_COORDINATION',
            network_size_estimate=1,
            coordination_sophistication='NONE',
            campaign_indicators={},
            temporal_coordination={},
            content_coordination={},
            behavioral_coordination={}
        )
