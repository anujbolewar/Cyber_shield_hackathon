#!/usr/bin/env python3
"""
🐦 LIVE TWITTER MONITORING SYSTEM
Real-time Twitter monitoring for law enforcement
Includes sentiment analysis, bot detection, and evidence capture
"""

import os
import sys
import json
import time
import threading
import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from enum import Enum
import requests
import uuid

# Twitter API simulation (replace with actual Twitter API v2)
class TwitterAPIv2:
    """
    🐦 Twitter API v2 interface for live streaming
    Replace with actual Twitter API implementation
    """
    
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self.stream_active = False
    
    def create_stream_rule(self, rules: List[Dict[str, str]]) -> Dict[str, Any]:
        """Create filtering rules for the stream"""
        # Simulate API response
        return {
            "data": [
                {"value": rule["value"], "tag": rule.get("tag", ""), "id": str(uuid.uuid4())}
                for rule in rules
            ]
        }
    
    def start_filtered_stream(self, callback_function):
        """Start filtered stream with callback"""
        self.stream_active = True
        
        # Simulate streaming tweets
        def simulate_stream():
            while self.stream_active:
                # Generate simulated tweet data
                simulated_tweet = self._generate_simulated_tweet()
                callback_function(simulated_tweet)
                time.sleep(2)  # Stream every 2 seconds
        
        stream_thread = threading.Thread(target=simulate_stream, daemon=True)
        stream_thread.start()
        return stream_thread
    
    def stop_stream(self):
        """Stop the active stream"""
        self.stream_active = False
    
    def _generate_simulated_tweet(self) -> Dict[str, Any]:
        """Generate simulated tweet data for testing"""
        import random
        
        # Sample India-related content
        india_content = [
            "Traffic update: Heavy congestion on Mumbai-Pune highway due to accident near Lonavala",
            "Delhi police conducting awareness drive about cyber security in schools",
            "Bangalore tech meetup discussing AI applications in governance",
            "Chennai floods: Emergency services coordinating relief efforts",
            "Kolkata cultural festival celebrating traditional Bengali art forms",
            "Hyderabad startup announces breakthrough in clean energy technology",
            "Pune students organize cleanliness drive in local communities",
            "Jaipur tourism board promotes heritage sites through digital campaigns"
        ]
        
        # Sample locations
        locations = [
            {"place": "Mumbai, Maharashtra", "coordinates": [19.0760, 72.8777]},
            {"place": "Delhi, India", "coordinates": [28.7041, 77.1025]},
            {"place": "Bangalore, Karnataka", "coordinates": [12.9716, 77.5946]},
            {"place": "Chennai, Tamil Nadu", "coordinates": [13.0827, 80.2707]},
            {"place": "Kolkata, West Bengal", "coordinates": [22.5726, 88.3639]},
            {"place": "Hyderabad, Telangana", "coordinates": [17.3850, 78.4867]}
        ]
        
        location = random.choice(locations)
        
        return {
            "data": {
                "id": str(random.randint(1000000000000000000, 9999999999999999999)),
                "text": random.choice(india_content),
                "created_at": datetime.now().isoformat(),
                "author_id": str(random.randint(100000000, 999999999)),
                "public_metrics": {
                    "retweet_count": random.randint(0, 50),
                    "like_count": random.randint(0, 200),
                    "reply_count": random.randint(0, 20),
                    "quote_count": random.randint(0, 10)
                },
                "geo": {
                    "place_id": str(uuid.uuid4()),
                    "coordinates": location["coordinates"]
                }
            },
            "includes": {
                "users": [{
                    "id": str(random.randint(100000000, 999999999)),
                    "username": f"user_{random.randint(1000, 9999)}",
                    "name": f"User {random.randint(1000, 9999)}",
                    "verified": random.choice([True, False]),
                    "public_metrics": {
                        "followers_count": random.randint(10, 10000),
                        "following_count": random.randint(10, 1000),
                        "tweet_count": random.randint(100, 50000)
                    }
                }],
                "places": [{
                    "id": str(uuid.uuid4()),
                    "name": location["place"],
                    "country": "India",
                    "geo": {
                        "type": "Point",
                        "coordinates": location["coordinates"]
                    }
                }]
            }
        }

@dataclass
class TweetData:
    """Data structure for processed tweet information"""
    tweet_id: str
    text: str
    author_id: str
    author_username: str
    created_at: datetime
    location: Optional[str]
    coordinates: Optional[Tuple[float, float]]
    retweet_count: int
    like_count: int
    reply_count: int
    quote_count: int
    sentiment_score: float
    threat_level: str
    bot_probability: float
    engagement_velocity: float
    keywords_matched: List[str]

class ThreatLevel(Enum):
    """Threat level classifications"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class LiveTwitterMonitor:
    """
    🐦 Comprehensive live Twitter monitoring system
    Real-time analysis and alerting for law enforcement
    """
    
    def __init__(self, bearer_token: str = "demo_token"):
        """Initialize Twitter monitoring system"""
        self.logger = self._setup_logging()
        self.twitter_api = TwitterAPIv2(bearer_token)
        self.db_path = self._initialize_database()
        self.is_monitoring = False
        self.stream_thread = None
        
        # India-related keywords for filtering
        self.india_keywords = [
            "India", "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad",
            "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore",
            "police", "security", "emergency", "traffic", "crime", "safety",
            "government", "politics", "protest", "rally", "election",
            "terrorism", "bomb", "threat", "violence", "attack"
        ]
        
        # Threat keywords
        self.threat_keywords = {
            "HIGH": ["bomb", "attack", "terrorism", "threat", "violence", "kill", "murder"],
            "MEDIUM": ["protest", "rally", "riot", "fight", "weapon", "danger"],
            "LOW": ["suspicious", "concern", "worry", "problem", "issue"]
        }
        
        print("🐦 Live Twitter Monitor initialized")
        print(f"   🔑 API Status: {'Connected' if bearer_token != 'demo_token' else 'Demo Mode'}")
        print(f"   🎯 Keywords: {len(self.india_keywords)} India-related terms")
        print(f"   🚨 Threat Detection: {sum(len(words) for words in self.threat_keywords.values())} patterns")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for Twitter monitoring"""
        logger = logging.getLogger("TwitterMonitor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Create logs directory
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # File handler
            file_handler = logging.FileHandler(log_dir / "twitter_monitor.log")
            console_handler = logging.StreamHandler()
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_database(self) -> str:
        """Initialize database for storing tweets and analysis"""
        db_dir = Path("data")
        db_dir.mkdir(exist_ok=True)
        
        db_path = db_dir / "twitter_monitor.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tweets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                author_id TEXT NOT NULL,
                author_username TEXT,
                created_at TEXT NOT NULL,
                location TEXT,
                latitude REAL,
                longitude REAL,
                retweet_count INTEGER DEFAULT 0,
                like_count INTEGER DEFAULT 0,
                reply_count INTEGER DEFAULT 0,
                quote_count INTEGER DEFAULT 0,
                sentiment_score REAL,
                threat_level TEXT,
                bot_probability REAL,
                engagement_velocity REAL,
                keywords_matched TEXT,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS twitter_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                acknowledged INTEGER DEFAULT 0,
                FOREIGN KEY (tweet_id) REFERENCES tweets (id)
            )
        """)
        
        # User tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS twitter_users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                display_name TEXT,
                verified INTEGER DEFAULT 0,
                followers_count INTEGER DEFAULT 0,
                following_count INTEGER DEFAULT 0,
                tweet_count INTEGER DEFAULT 0,
                bot_score REAL DEFAULT 0.0,
                risk_level TEXT DEFAULT 'LOW',
                first_seen TEXT DEFAULT CURRENT_TIMESTAMP,
                last_seen TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Geographic clusters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS geo_clusters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cluster_name TEXT NOT NULL,
                center_lat REAL NOT NULL,
                center_lng REAL NOT NULL,
                radius_km REAL NOT NULL,
                tweet_count INTEGER DEFAULT 0,
                threat_score REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        return str(db_path)
    
    def start_monitoring(self) -> bool:
        """
        🚀 Start live Twitter monitoring
        """
        try:
            if self.is_monitoring:
                self.logger.warning("Monitoring already active")
                return False
            
            print("\n🚀 STARTING LIVE TWITTER MONITORING")
            print("=" * 60)
            
            # Create stream rules
            stream_rules = [
                {
                    "value": " OR ".join(self.india_keywords[:10]),  # First 10 keywords
                    "tag": "india_general"
                },
                {
                    "value": " OR ".join(self.threat_keywords["HIGH"]),
                    "tag": "high_threat"
                },
                {
                    "value": " OR ".join(self.threat_keywords["MEDIUM"]),
                    "tag": "medium_threat"
                }
            ]
            
            # Set up stream rules
            rules_response = self.twitter_api.create_stream_rule(stream_rules)
            print(f"   ✅ Stream rules created: {len(rules_response.get('data', []))} rules")
            
            # Start streaming
            self.stream_thread = self.twitter_api.start_filtered_stream(self._process_tweet)
            self.is_monitoring = True
            
            print(f"   ✅ Live stream started")
            print(f"   ✅ Processing tweets in real-time")
            print(f"   ✅ Database: {self.db_path}")
            
            self.logger.info("Twitter monitoring started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {str(e)}")
            print(f"   ❌ Error starting monitoring: {str(e)}")
            return False
    
    def stop_monitoring(self) -> bool:
        """
        🛑 Stop live Twitter monitoring
        """
        try:
            if not self.is_monitoring:
                self.logger.warning("Monitoring not active")
                return False
            
            print("\n🛑 STOPPING TWITTER MONITORING")
            print("=" * 60)
            
            # Stop the stream
            self.twitter_api.stop_stream()
            self.is_monitoring = False
            
            if self.stream_thread:
                self.stream_thread.join(timeout=5)
            
            print("   ✅ Stream stopped")
            print("   ✅ Monitoring deactivated")
            
            self.logger.info("Twitter monitoring stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {str(e)}")
            return False
    
    def _process_tweet(self, tweet_data: Dict[str, Any]):
        """
        🔄 Process incoming tweet data
        """
        try:
            # Extract tweet information
            tweet = tweet_data.get("data", {})
            includes = tweet_data.get("includes", {})
            users = includes.get("users", [])
            places = includes.get("places", [])
            
            # Get user information
            user = users[0] if users else {}
            place = places[0] if places else {}
            
            # Create TweetData object
            tweet_obj = TweetData(
                tweet_id=tweet.get("id", ""),
                text=tweet.get("text", ""),
                author_id=tweet.get("author_id", ""),
                author_username=user.get("username", ""),
                created_at=datetime.fromisoformat(tweet.get("created_at", datetime.now().isoformat()).replace('Z', '+00:00')),
                location=place.get("name"),
                coordinates=self._extract_coordinates(tweet.get("geo", {})),
                retweet_count=tweet.get("public_metrics", {}).get("retweet_count", 0),
                like_count=tweet.get("public_metrics", {}).get("like_count", 0),
                reply_count=tweet.get("public_metrics", {}).get("reply_count", 0),
                quote_count=tweet.get("public_metrics", {}).get("quote_count", 0),
                sentiment_score=0.0,  # Will be calculated
                threat_level="LOW",   # Will be calculated
                bot_probability=0.0,  # Will be calculated
                engagement_velocity=0.0,  # Will be calculated
                keywords_matched=[]   # Will be populated
            )
            
            # Perform analysis
            self._analyze_sentiment(tweet_obj)
            self._detect_threat_level(tweet_obj)
            self._calculate_bot_probability(tweet_obj, user)
            self._calculate_engagement_velocity(tweet_obj)
            self._match_keywords(tweet_obj)
            
            # Store in database
            self._store_tweet(tweet_obj)
            self._store_user(user)
            
            # Update geographic clustering
            if tweet_obj.coordinates:
                self._update_geo_clusters(tweet_obj)
            
            # Generate alerts if necessary
            self._generate_alerts(tweet_obj)
            
            # Capture evidence if high priority
            if tweet_obj.threat_level in ["HIGH", "CRITICAL"]:
                self._capture_evidence(tweet_obj)
            
            print(f"🐦 Processed: {tweet_obj.tweet_id[:10]}... | Threat: {tweet_obj.threat_level} | Sentiment: {tweet_obj.sentiment_score:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error processing tweet: {str(e)}")
    
    def _analyze_sentiment(self, tweet: TweetData):
        """
        😊 Analyze tweet sentiment
        """
        text = tweet.text.lower()
        
        # Simple sentiment analysis (replace with advanced NLP)
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy", "love", "best", "awesome", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "sad", "angry", "disappointed", "furious"]
        threat_words = ["kill", "bomb", "attack", "threat", "violence", "murder", "terror", "destroy"]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        threat_count = sum(1 for word in threat_words if word in text)
        
        # Calculate sentiment score (-1 to 1)
        if threat_count > 0:
            tweet.sentiment_score = -0.8 - (threat_count * 0.1)
        else:
            total_sentiment_words = positive_count + negative_count
            if total_sentiment_words > 0:
                tweet.sentiment_score = (positive_count - negative_count) / total_sentiment_words
            else:
                tweet.sentiment_score = 0.0
        
        # Clamp to [-1, 1] range
        tweet.sentiment_score = max(-1.0, min(1.0, tweet.sentiment_score))
    
    def _detect_threat_level(self, tweet: TweetData):
        """
        🚨 Detect threat level in tweet
        """
        text = tweet.text.lower()
        
        # Check for high threat keywords
        high_threat_matches = sum(1 for word in self.threat_keywords["HIGH"] if word in text)
        medium_threat_matches = sum(1 for word in self.threat_keywords["MEDIUM"] if word in text)
        low_threat_matches = sum(1 for word in self.threat_keywords["LOW"] if word in text)
        
        # Determine threat level
        if high_threat_matches > 0 or tweet.sentiment_score < -0.7:
            tweet.threat_level = "HIGH"
        elif medium_threat_matches > 0 or tweet.sentiment_score < -0.4:
            tweet.threat_level = "MEDIUM"
        elif low_threat_matches > 0 or tweet.sentiment_score < -0.2:
            tweet.threat_level = "LOW"
        else:
            tweet.threat_level = "LOW"
        
        # Escalate to CRITICAL if multiple high-threat indicators
        if high_threat_matches >= 2 and tweet.sentiment_score < -0.8:
            tweet.threat_level = "CRITICAL"
    
    def _calculate_bot_probability(self, tweet: TweetData, user_data: Dict[str, Any]):
        """
        🤖 Calculate probability that user is a bot
        """
        bot_score = 0.0
        
        # Analyze user metrics
        followers = user_data.get("public_metrics", {}).get("followers_count", 0)
        following = user_data.get("public_metrics", {}).get("following_count", 0)
        tweets = user_data.get("public_metrics", {}).get("tweet_count", 0)
        
        # Bot indicators
        # 1. Unrealistic follower-to-following ratio
        if following > 0:
            ratio = followers / following
            if ratio > 100 or ratio < 0.01:
                bot_score += 0.3
        
        # 2. Excessive tweet count
        if tweets > 50000:
            bot_score += 0.2
        
        # 3. Generic username pattern
        username = user_data.get("username", "")
        if re.match(r"^user\d+$", username.lower()):
            bot_score += 0.3
        
        # 4. Tweet content analysis
        text = tweet.text
        if len(text) < 20:  # Very short tweets
            bot_score += 0.1
        
        # 5. Repetitive content (would need historical analysis)
        # Placeholder for more sophisticated analysis
        
        tweet.bot_probability = min(1.0, bot_score)
    
    def _calculate_engagement_velocity(self, tweet: TweetData):
        """
        📈 Calculate engagement velocity (engagement per minute)
        """
        # Calculate time since tweet creation
        now = datetime.now()
        if tweet.created_at.tzinfo is not None:
            now = now.replace(tzinfo=tweet.created_at.tzinfo)
        
        time_diff = (now - tweet.created_at).total_seconds() / 60  # minutes
        
        if time_diff > 0:
            total_engagement = (
                tweet.retweet_count + 
                tweet.like_count + 
                tweet.reply_count + 
                tweet.quote_count
            )
            tweet.engagement_velocity = total_engagement / time_diff
        else:
            tweet.engagement_velocity = 0.0
    
    def _match_keywords(self, tweet: TweetData):
        """
        🔍 Match keywords in tweet text
        """
        text = tweet.text.lower()
        matched_keywords = []
        
        # Check India keywords
        for keyword in self.india_keywords:
            if keyword.lower() in text:
                matched_keywords.append(keyword)
        
        # Check threat keywords
        for level, keywords in self.threat_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    matched_keywords.append(f"{keyword} ({level})")
        
        tweet.keywords_matched = matched_keywords
    
    def _extract_coordinates(self, geo_data: Dict[str, Any]) -> Optional[Tuple[float, float]]:
        """Extract coordinates from geo data"""
        if not geo_data:
            return None
        
        coordinates = geo_data.get("coordinates")
        if coordinates and len(coordinates) >= 2:
            return (float(coordinates[0]), float(coordinates[1]))
        
        return None
    
    def _store_tweet(self, tweet: TweetData):
        """
        💾 Store tweet in database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO tweets (
                    id, text, author_id, author_username, created_at, location,
                    latitude, longitude, retweet_count, like_count, reply_count,
                    quote_count, sentiment_score, threat_level, bot_probability,
                    engagement_velocity, keywords_matched
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tweet.tweet_id,
                tweet.text,
                tweet.author_id,
                tweet.author_username,
                tweet.created_at.isoformat(),
                tweet.location,
                tweet.coordinates[0] if tweet.coordinates else None,
                tweet.coordinates[1] if tweet.coordinates else None,
                tweet.retweet_count,
                tweet.like_count,
                tweet.reply_count,
                tweet.quote_count,
                tweet.sentiment_score,
                tweet.threat_level,
                tweet.bot_probability,
                tweet.engagement_velocity,
                json.dumps(tweet.keywords_matched)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error storing tweet: {str(e)}")
    
    def _store_user(self, user_data: Dict[str, Any]):
        """
        👤 Store user information in database
        """
        try:
            if not user_data:
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            metrics = user_data.get("public_metrics", {})
            
            cursor.execute("""
                INSERT OR REPLACE INTO twitter_users (
                    user_id, username, display_name, verified,
                    followers_count, following_count, tweet_count,
                    last_seen
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_data.get("id"),
                user_data.get("username"),
                user_data.get("name"),
                1 if user_data.get("verified") else 0,
                metrics.get("followers_count", 0),
                metrics.get("following_count", 0),
                metrics.get("tweet_count", 0),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error storing user: {str(e)}")
    
    def _update_geo_clusters(self, tweet: TweetData):
        """
        🗺️ Update geographic clustering
        """
        if not tweet.coordinates:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            lat, lng = tweet.coordinates
            
            # Find nearby clusters (within 10km)
            cursor.execute("""
                SELECT id, cluster_name, center_lat, center_lng, tweet_count, threat_score
                FROM geo_clusters
                WHERE (
                    6371 * acos(
                        cos(radians(?)) * cos(radians(center_lat)) *
                        cos(radians(center_lng) - radians(?)) +
                        sin(radians(?)) * sin(radians(center_lat))
                    )
                ) < 10
            """, (lat, lng, lat))
            
            nearby_cluster = cursor.fetchone()
            
            threat_score_map = {"LOW": 1, "MEDIUM": 3, "HIGH": 7, "CRITICAL": 10}
            tweet_threat_score = threat_score_map.get(tweet.threat_level, 1)
            
            if nearby_cluster:
                # Update existing cluster
                cluster_id, name, center_lat, center_lng, count, threat_score = nearby_cluster
                
                new_count = count + 1
                new_threat_score = (threat_score * count + tweet_threat_score) / new_count
                
                cursor.execute("""
                    UPDATE geo_clusters
                    SET tweet_count = ?, threat_score = ?, updated_at = ?
                    WHERE id = ?
                """, (new_count, new_threat_score, datetime.now().isoformat(), cluster_id))
            else:
                # Create new cluster
                cluster_name = f"Cluster_{tweet.location or 'Unknown'}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                
                cursor.execute("""
                    INSERT INTO geo_clusters (
                        cluster_name, center_lat, center_lng, radius_km,
                        tweet_count, threat_score
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (cluster_name, lat, lng, 5.0, 1, tweet_threat_score))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error updating geo clusters: {str(e)}")
    
    def _generate_alerts(self, tweet: TweetData):
        """
        🚨 Generate automatic alerts for high-priority tweets
        """
        try:
            should_alert = False
            alert_type = ""
            priority = "LOW"
            message = ""
            
            # High threat level
            if tweet.threat_level in ["HIGH", "CRITICAL"]:
                should_alert = True
                alert_type = "THREAT_DETECTED"
                priority = tweet.threat_level
                message = f"High threat tweet detected: {tweet.text[:100]}..."
            
            # High bot probability with negative sentiment
            elif tweet.bot_probability > 0.7 and tweet.sentiment_score < -0.5:
                should_alert = True
                alert_type = "BOT_NEGATIVE_SENTIMENT"
                priority = "MEDIUM"
                message = f"Potential bot spreading negative content: @{tweet.author_username}"
            
            # High engagement velocity on negative content
            elif tweet.engagement_velocity > 50 and tweet.sentiment_score < -0.3:
                should_alert = True
                alert_type = "VIRAL_NEGATIVE_CONTENT"
                priority = "MEDIUM"
                message = f"Negative content going viral: {tweet.engagement_velocity:.1f} engagements/min"
            
            # Geographic clustering alert
            elif tweet.coordinates and tweet.threat_level != "LOW":
                should_alert = True
                alert_type = "GEO_CLUSTER_THREAT"
                priority = "MEDIUM"
                message = f"Threat detected in geographic cluster: {tweet.location}"
            
            if should_alert:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO twitter_alerts (
                        tweet_id, alert_type, priority, message
                    ) VALUES (?, ?, ?, ?)
                """, (tweet.tweet_id, alert_type, priority, message))
                
                conn.commit()
                conn.close()
                
                print(f"🚨 ALERT: {priority} - {message}")
                self.logger.warning(f"Alert generated: {alert_type} - {message}")
            
        except Exception as e:
            self.logger.error(f"Error generating alerts: {str(e)}")
    
    def _capture_evidence(self, tweet: TweetData):
        """
        📸 Capture evidence screenshot for high-priority tweets
        """
        try:
            # Create evidence directory
            evidence_dir = Path("evidence/twitter")
            evidence_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate evidence metadata
            evidence_data = {
                "tweet_id": tweet.tweet_id,
                "capture_timestamp": datetime.now().isoformat(),
                "tweet_content": tweet.text,
                "author": tweet.author_username,
                "threat_level": tweet.threat_level,
                "sentiment_score": tweet.sentiment_score,
                "bot_probability": tweet.bot_probability,
                "location": tweet.location,
                "coordinates": tweet.coordinates,
                "keywords_matched": tweet.keywords_matched,
                "evidence_hash": hashlib.sha256(tweet.text.encode()).hexdigest()[:16]
            }
            
            # Save evidence metadata
            evidence_file = evidence_dir / f"evidence_{tweet.tweet_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(evidence_file, 'w') as f:
                json.dump(evidence_data, f, indent=2, default=str)
            
            print(f"📸 Evidence captured: {evidence_file.name}")
            self.logger.info(f"Evidence captured for tweet {tweet.tweet_id}")
            
        except Exception as e:
            self.logger.error(f"Error capturing evidence: {str(e)}")
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """
        📊 Get current monitoring statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total tweets processed
            cursor.execute("SELECT COUNT(*) FROM tweets")
            total_tweets = cursor.fetchone()[0]
            
            # Tweets by threat level
            cursor.execute("""
                SELECT threat_level, COUNT(*) 
                FROM tweets 
                GROUP BY threat_level
            """)
            threat_distribution = dict(cursor.fetchall())
            
            # Recent alerts
            cursor.execute("""
                SELECT COUNT(*) 
                FROM twitter_alerts 
                WHERE datetime(created_at) > datetime('now', '-1 hour')
            """)
            recent_alerts = cursor.fetchone()[0]
            
            # Geographic clusters
            cursor.execute("SELECT COUNT(*) FROM geo_clusters")
            geo_clusters = cursor.fetchone()[0]
            
            # Bot detection stats
            cursor.execute("""
                SELECT AVG(bot_probability), COUNT(*) 
                FROM tweets 
                WHERE bot_probability > 0.7
            """)
            bot_stats = cursor.fetchone()
            avg_bot_prob = bot_stats[0] if bot_stats[0] else 0.0
            high_bot_count = bot_stats[1]
            
            conn.close()
            
            return {
                "monitoring_active": self.is_monitoring,
                "total_tweets_processed": total_tweets,
                "threat_distribution": threat_distribution,
                "recent_alerts_1h": recent_alerts,
                "geographic_clusters": geo_clusters,
                "average_bot_probability": round(avg_bot_prob, 3),
                "high_bot_probability_tweets": high_bot_count,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stats: {str(e)}")
            return {"error": str(e)}


def test_twitter_monitoring():
    """Test the Twitter monitoring system"""
    print("\n🧪 TESTING LIVE TWITTER MONITORING")
    print("=" * 80)
    
    # Initialize monitor
    monitor = LiveTwitterMonitor("demo_bearer_token")
    
    # Test 1: Start monitoring
    print("\n1️⃣ Testing Monitor Startup...")
    start_result = monitor.start_monitoring()
    print(f"   Status: {'✅ STARTED' if start_result else '❌ FAILED'}")
    
    if start_result:
        # Let it run for a few seconds to collect data
        print("   📡 Collecting sample tweets...")
        time.sleep(10)
        
        # Test 2: Get statistics
        print("\n2️⃣ Testing Statistics Collection...")
        stats = monitor.get_monitoring_stats()
        has_stats = "total_tweets_processed" in stats and stats["total_tweets_processed"] > 0
        print(f"   Status: {'✅ COLLECTED' if has_stats else '❌ NO DATA'}")
        
        if has_stats:
            print(f"      📊 Tweets Processed: {stats['total_tweets_processed']}")
            print(f"      🚨 Recent Alerts: {stats['recent_alerts_1h']}")
            print(f"      🤖 High Bot Probability: {stats['high_bot_probability_tweets']}")
            print(f"      🗺️ Geographic Clusters: {stats['geographic_clusters']}")
        
        # Test 3: Stop monitoring
        print("\n3️⃣ Testing Monitor Shutdown...")
        stop_result = monitor.stop_monitoring()
        print(f"   Status: {'✅ STOPPED' if stop_result else '❌ FAILED'}")
    
    # Test 4: Database validation
    print("\n4️⃣ Testing Database Structure...")
    db_path = Path(monitor.db_path)
    db_exists = db_path.exists()
    print(f"   Status: {'✅ EXISTS' if db_exists else '❌ MISSING'}")
    
    # Summary
    print(f"\n📊 TWITTER MONITORING TEST SUMMARY")
    print("=" * 80)
    
    results = [
        ('Monitor Startup', start_result),
        ('Statistics Collection', has_stats if start_result else False),
        ('Monitor Shutdown', stop_result if start_result else False),
        ('Database Structure', db_exists)
    ]
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall Success Rate: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🏆 TWITTER MONITORING SYSTEM FULLY OPERATIONAL!")
    elif passed_tests >= total_tests * 0.8:
        print("🥇 TWITTER MONITORING SYSTEM WORKING WELL!")
    else:
        print("⚠️ TWITTER MONITORING SYSTEM NEEDS ATTENTION")
    
    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': passed_tests / total_tests,
        'results': dict(results)
    }


if __name__ == "__main__":
    test_twitter_monitoring()
