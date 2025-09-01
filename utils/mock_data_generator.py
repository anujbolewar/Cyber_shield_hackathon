"""
Mock Data Generator for Police AI Monitoring System
Generates realistic social media data for cyber threat detection demonstrations
"""

import random
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import uuid

class PoliceAIDataGenerator:
    """Generate realistic mock data for police cyber monitoring demonstrations"""
    
    def __init__(self):
        # Indian names and locations
        self.indian_first_names = [
            "Rajesh", "Priya", "Amit", "Neha", "Suresh", "Kavya", "Vikram", "Anjali",
            "Ravi", "Pooja", "Sanjay", "Meera", "Ashok", "Deepika", "Manoj", "Shreya",
            "Kiran", "Anita", "Rohit", "Sunita", "Ajay", "Nisha", "Pramod", "Rekha",
            "Vinod", "Geeta", "Ramesh", "Sita", "Mohan", "Radha", "Krishnan", "Lakshmi",
            "Arjun", "Gayatri", "Harish", "Preethi", "Dinesh", "Shanti", "Mahesh", "Kamala",
            "Ahmed", "Fatima", "Mohammed", "Aisha", "Hassan", "Zara", "Ali", "Sakina",
            "David", "Mary", "John", "Susan", "Thomas", "Grace", "Michael", "Rose"
        ]
        
        self.indian_last_names = [
            "Sharma", "Patel", "Kumar", "Singh", "Gupta", "Agarwal", "Jain", "Mishra",
            "Yadav", "Verma", "Rajput", "Mehta", "Shah", "Reddy", "Nair", "Pillai",
            "Iyer", "Menon", "Rao", "Krishnan", "Bhat", "Shetty", "Kaul", "Malhotra",
            "Khan", "Sheikh", "Malik", "Ansari", "Qureshi", "Siddiqui", "Rahman", "Ali",
            "Das", "Roy", "Banerjee", "Chatterjee", "Ghosh", "Mukherjee", "Sen", "Bose",
            "Fernandes", "D'Souza", "Pereira", "Rodrigues", "Gomes", "Lobo", "Costa", "Dsouza"
        ]
        
        self.indian_cities = [
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad",
            "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
            "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad",
            "Meerut", "Rajkot", "Kalyan", "Vasai", "Varanasi", "Srinagar", "Dhanbad", "Jodhpur",
            "Amritsar", "Raipur", "Allahabad", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Madurai",
            "Guwahati", "Chandigarh", "Hubli", "Mysore", "Tiruchirappalli", "Bareilly", "Aligarh", "Tiruppur",
            "Gurgaon", "Moradabad", "Jalandhar", "Bhubaneswar", "Salem", "Warangal", "Guntur", "Bhiwandi",
            "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Cuttack"
        ]
        
        self.platforms = ["Twitter", "Facebook", "Instagram", "Telegram", "WhatsApp", "YouTube", "TikTok"]
        
        # Threat keywords for different categories
        self.terrorism_keywords = [
            "bomb", "blast", "attack", "kill", "destroy", "ISIS", "jihad", "terror", "explosive",
            "suicide", "martyr", "revenge", "strike", "target", "operation", "cell", "recruit"
        ]
        
        self.anti_national_keywords = [
            "traitor", "anti-national", "Pakistan", "zindabad", "murdabad", "Kashmir", "azadi",
            "independence", "separatist", "occupation", "freedom", "resistance", "liberation"
        ]
        
        self.cybercrime_keywords = [
            "hack", "credit card", "bank", "fraud", "scam", "bitcoin", "cryptocurrency", "phishing",
            "malware", "ransomware", "data breach", "stolen", "account", "password", "dark web"
        ]
        
        # Normal content templates
        self.normal_content_templates = [
            "Had a great day at {location} with family! #family #fun",
            "Beautiful sunset today in {location}. Nature is amazing! 🌅",
            "Just finished watching {movie}. Loved it! #movies #entertainment",
            "Morning workout complete! Feeling energetic 💪 #fitness #health",
            "Delicious {food} at {restaurant} in {location}. Highly recommended! #food",
            "Happy {festival}! Celebrating with friends and family 🎉",
            "Work from home today. Productivity level: {level}/10 #workfromhome",
            "Weekend plans: {activity} with friends! #weekend #friends",
            "Traffic is crazy in {location} today 🚗 #traffic #citylife",
            "New book recommendation: {book}. Great read! #books #reading"
        ]
        
        # Suspicious content templates
        self.suspicious_templates = [
            "Government is corrupt! Time for revolution! #change #protest",
            "These politicians need to go! Enough is enough! #politics #anger",
            "System is broken. We need to take action! #justice #reform",
            "Media is lying to us! Wake up people! #truth #awareness",
            "Economic policies are destroying our country! #economy #crisis"
        ]
        
        # High-risk content templates
        self.high_risk_templates = [
            "भारत सरकार को {action} करना होगा। {threat_keyword} का उपयोग करके।",
            "Pakistan {support_word}! भारत {oppose_word}! Kashmir needs {freedom_word}!",
            "Time to {action_word} the {target}. We have the {weapon} ready.",
            "Join our {group_type} for the upcoming {operation}. Contact {contact_method}.",
            "Selling {illegal_item}. Payment in {crypto}. Secure delivery guaranteed.",
            "{threat_keyword} attack planned for {date}. Join us! #{hashtag}",
            "Government officials are {threat_word}. Time for {action}! #revolution",
            "Anti-national elements must be {action}. Support our cause! #{tag}"
        ]
        
        # Bot behavior patterns
        self.bot_patterns = [
            "Follow @{username1} Follow @{username2} Follow @{username3} #followback",
            "URGENT!!! {message} SHARE IMMEDIATELY!!! #viral #breaking",
            "🚨 ALERT 🚨 {content} RT if you agree! #important #share",
            "Breaking: {news} Everyone must know! Retweet! #news #urgent",
            "💯 TRUTH: {statement} Share to spread awareness! #truth #wakeup"
        ]
        
        # Common Hindi phrases
        self.hindi_phrases = [
            "बहुत अच्छा", "धन्यवाद", "नमस्ते", "आप कैसे हैं", "मजा आया",
            "शुभ प्रभात", "शुभ रात्रि", "हैप्पी बर्थडे", "बधाई हो", "शुक्रिया",
            "क्या बात है", "सच में", "वाह वाह", "मस्त है", "बहुत बढ़िया"
        ]
        
        # Generate consistent user data
        self.generated_users = {}
        self.generated_posts = []
        self.network_connections = {}
        
    def generate_username(self, user_type: str = "normal") -> str:
        """Generate realistic Indian usernames"""
        if user_type == "bot":
            patterns = [
                f"{random.choice(self.indian_first_names)}{random.randint(100, 9999)}",
                f"{random.choice(['real', 'official', 'verified'])}{random.choice(self.indian_first_names)}{random.randint(10, 999)}",
                f"{random.choice(self.indian_first_names)}{random.choice(['_official', '_real', '_verified', '_news'])}",
                f"{random.choice(['news', 'truth', 'fact'])}{random.choice(self.indian_first_names)}{random.randint(10, 99)}"
            ]
        else:
            patterns = [
                f"{random.choice(self.indian_first_names).lower()}{random.choice(self.indian_last_names).lower()}",
                f"{random.choice(self.indian_first_names).lower()}_{random.randint(80, 99)}",
                f"{random.choice(self.indian_first_names).lower()}.{random.choice(self.indian_last_names).lower()}",
                f"{random.choice(self.indian_first_names).lower()}{random.randint(1990, 2005)}",
                f"{random.choice(self.indian_cities).lower()}_{random.choice(self.indian_first_names).lower()}"
            ]
        
        return random.choice(patterns)
    
    def generate_user_profile(self, user_type: str = "normal") -> Dict[str, Any]:
        """Generate complete user profile"""
        username = self.generate_username(user_type)
        first_name = random.choice(self.indian_first_names)
        last_name = random.choice(self.indian_last_names)
        location = random.choice(self.indian_cities)
        
        # Account creation date
        if user_type == "bot":
            # Bots tend to have newer accounts
            account_age_days = random.randint(1, 180)
        else:
            account_age_days = random.randint(30, 3650)  # 1 month to 10 years
        
        account_created = datetime.now() - timedelta(days=account_age_days)
        
        # Follower patterns
        if user_type == "bot":
            followers = random.randint(50, 500)
            following = random.randint(200, 2000)  # Bots follow many
        elif user_type == "suspicious":
            followers = random.randint(100, 1000)
            following = random.randint(50, 300)
        else:
            followers = random.randint(20, 5000)
            following = random.randint(10, 800)
        
        profile = {
            "user_id": str(uuid.uuid4()),
            "username": username,
            "display_name": f"{first_name} {last_name}",
            "bio": self._generate_bio(user_type),
            "location": location,
            "verified": user_type == "normal" and random.random() < 0.05,  # 5% verified
            "followers_count": followers,
            "following_count": following,
            "posts_count": random.randint(10, 2000),
            "account_created": account_created.isoformat(),
            "profile_image": f"https://example.com/profiles/{username}.jpg",
            "user_type": user_type,
            "risk_score": self._calculate_user_risk_score(user_type),
            "platform": random.choice(self.platforms),
            "is_active": random.random() > 0.1,  # 90% active users
            "language_preference": random.choice(["hindi", "english", "mixed"]),
            "behavioral_indicators": self._generate_behavioral_indicators(user_type)
        }
        
        return profile
    
    def _generate_bio(self, user_type: str) -> str:
        """Generate user bio based on type"""
        if user_type == "bot":
            bios = [
                "🚨 Breaking News & Updates 📰 | Truth Seeker | Follow for Real News",
                "Official News Account | Verified Information | #TruthMatters",
                "📢 Important Updates Daily | Stay Informed | Real Facts Only",
                "News • Politics • Current Affairs | Independent Journalist",
                "🔥 Viral Content | Breaking Stories | Follow for Updates"
            ]
        elif user_type == "suspicious":
            bios = [
                "Patriot | Truth Seeker | Against Corruption | #JusticeForAll",
                "Fighting for Rights | Exposing Truth | Revolutionary Thinker",
                "Nationalist | Proud Indian | Against Anti-National Forces",
                "Freedom Fighter | Justice Warrior | Truth Speaker",
                "Defender of Faith | Protector of Culture | Real Patriot"
            ]
        else:
            bios = [
                f"Software Engineer at TechCorp | Love travel & photography | {random.choice(self.indian_cities)}",
                f"Teacher | Book lover | Foodie | Proud {random.choice(self.indian_cities)}kar",
                f"Doctor | Helping people | Family person | {random.choice(self.indian_cities)}",
                f"Student | Cricket fan | Music lover | Future entrepreneur",
                f"Businessman | Fitness enthusiast | {random.choice(self.indian_cities)} based",
                "🏏 Cricket • 📚 Books • 🎵 Music • ☕ Coffee",
                "Traveler | Photographer | Life is beautiful ✨",
                "Proud Indian 🇮🇳 | Family First | Work Hard Dream Big"
            ]
        
        return random.choice(bios)
    
    def _generate_behavioral_indicators(self, user_type: str) -> Dict[str, Any]:
        """Generate behavioral patterns for user types"""
        if user_type == "bot":
            return {
                "posting_frequency": "very_high",  # Multiple posts per hour
                "engagement_pattern": "artificial",  # Low genuine engagement
                "content_diversity": "low",  # Repetitive content
                "response_time": "instant",  # Immediate responses
                "activity_hours": "24x7",  # Round the clock activity
                "language_consistency": "inconsistent",  # Mixed quality
                "network_behavior": "suspicious",  # Following patterns
                "automation_score": random.uniform(0.7, 0.95)
            }
        elif user_type == "suspicious":
            return {
                "posting_frequency": "high",
                "engagement_pattern": "aggressive", 
                "content_diversity": "focused",  # Single topic focus
                "response_time": "quick",
                "activity_hours": "irregular",
                "language_consistency": "emotional",
                "network_behavior": "coordinated",
                "automation_score": random.uniform(0.2, 0.6)
            }
        else:
            return {
                "posting_frequency": "normal",
                "engagement_pattern": "organic",
                "content_diversity": "varied",
                "response_time": "natural",
                "activity_hours": "human_pattern",
                "language_consistency": "consistent",
                "network_behavior": "organic",
                "automation_score": random.uniform(0.0, 0.3)
            }
    
    def _calculate_user_risk_score(self, user_type: str) -> float:
        """Calculate risk score based on user type"""
        if user_type == "bot":
            return random.uniform(60, 90)
        elif user_type == "suspicious":
            return random.uniform(40, 80)
        else:
            return random.uniform(0, 30)
    
    def generate_social_media_post(self, user_profile: Dict[str, Any], 
                                 content_type: str = "normal") -> Dict[str, Any]:
        """Generate a social media post"""
        
        # Determine content based on type
        if content_type == "normal":
            content = self._generate_normal_content(user_profile)
            risk_score = random.uniform(0, 25)
        elif content_type == "suspicious":
            content = self._generate_suspicious_content(user_profile)
            risk_score = random.uniform(30, 60)
        elif content_type == "high_risk":
            content = self._generate_high_risk_content(user_profile)
            risk_score = random.uniform(70, 95)
        elif content_type == "bot":
            content = self._generate_bot_content(user_profile)
            risk_score = random.uniform(20, 70)
        else:
            content = self._generate_normal_content(user_profile)
            risk_score = random.uniform(0, 25)
        
        # Generate post metadata
        post_time = datetime.now() - timedelta(
            hours=random.randint(0, 168),  # Within last week
            minutes=random.randint(0, 59)
        )
        
        post = {
            "post_id": str(uuid.uuid4()),
            "user_id": user_profile["user_id"],
            "username": user_profile["username"],
            "content": content,
            "timestamp": post_time.isoformat(),
            "platform": user_profile["platform"],
            "content_type": content_type,
            "risk_score": risk_score,
            "location": user_profile["location"],
            "language": self._detect_language(content),
            "engagement": self._generate_engagement_metrics(user_profile, content_type),
            "hashtags": self._extract_hashtags(content),
            "mentions": self._extract_mentions(content),
            "media_attachments": self._generate_media_attachments(),
            "ip_metadata": self._generate_ip_metadata(user_profile),
            "device_info": self._generate_device_info(),
            "threat_indicators": self._analyze_threat_indicators(content, content_type)
        }
        
        return post
    
    def _generate_normal_content(self, user_profile: Dict[str, Any]) -> str:
        """Generate normal, benign content"""
        templates = self.normal_content_templates.copy()
        
        # Add Hindi content for mixed language users
        if user_profile.get("language_preference") in ["hindi", "mixed"]:
            hindi_templates = [
                "आज बहुत अच्छा दिन था! परिवार के साथ समय बिताया। #family",
                "मुंबई में बारिश हो रही है। मौसम बहुत सुहावना है! 🌧️",
                "नई फिल्म देखी आज। बहुत पसंद आई! #bollywood #movies",
                "सुबह की योग कक्षा पूरी की। स्वस्थ रहना जरूरी है! #yoga #health",
                "दोस्तों के साथ पार्टी का प्लान है। #weekend #friends"
            ]
            templates.extend(hindi_templates)
        
        template = random.choice(templates)
        
        # Fill placeholders
        content = template.format(
            location=random.choice(self.indian_cities),
            movie=random.choice(["RRR", "Pushpa", "KGF", "Dangal", "3 Idiots"]),
            food=random.choice(["biryani", "dosa", "samosa", "chole bhature", "butter chicken"]),
            restaurant=f"{random.choice(['Cafe', 'Restaurant', 'Dhaba'])} {random.choice(self.indian_first_names)}",
            festival=random.choice(["Diwali", "Holi", "Eid", "Christmas", "Navratri"]),
            level=random.randint(6, 10),
            activity=random.choice(["shopping", "movie", "picnic", "temple visit", "cricket match"]),
            book=random.choice(["Gitanjali", "The God of Small Things", "Midnight's Children"])
        )
        
        return content
    
    def _generate_suspicious_content(self, user_profile: Dict[str, Any]) -> str:
        """Generate suspicious but not explicitly threatening content"""
        template = random.choice(self.suspicious_templates)
        
        return template
    
    def _generate_high_risk_content(self, user_profile: Dict[str, Any]) -> str:
        """Generate high-risk threatening content"""
        template = random.choice(self.high_risk_templates)
        
        # Fill dangerous placeholders
        content = template.format(
            action=random.choice(["नष्ट", "उखाड़", "हटा", "बदल"]),
            threat_keyword=random.choice(self.terrorism_keywords),
            support_word=random.choice(["zindabad", "jindabad", "की जय"]),
            oppose_word=random.choice(["murdabad", "मुर्दाबाद", "down"]),
            freedom_word=random.choice(["azadi", "स्वतंत्रता", "freedom"]),
            action_word=random.choice(["eliminate", "remove", "destroy", "attack"]),
            target=random.choice(["government", "system", "corrupt officials"]),
            weapon=random.choice(["plan", "resources", "support", "network"]),
            group_type=random.choice(["movement", "organization", "cell", "group"]),
            operation=random.choice(["mission", "operation", "action", "strike"]),
            contact_method=random.choice(["telegram", "encrypted chat", "secure channel"]),
            illegal_item=random.choice(["weapons", "explosives", "data", "documents"]),
            crypto=random.choice(["Bitcoin", "cryptocurrency", "digital currency"]),
            date=random.choice(["tomorrow", "next week", "soon", "15th August"]),
            hashtag=random.choice(["revolution", "freedom", "justice", "action"]),
            threat_word=random.choice(["enemies", "traitors", "corrupt", "anti-national"]),
            tag=random.choice(["patriot", "justice", "truth", "action"])
        )
        
        return content
    
    def _generate_bot_content(self, user_profile: Dict[str, Any]) -> str:
        """Generate bot-like content"""
        template = random.choice(self.bot_patterns)
        
        content = template.format(
            username1=self.generate_username("bot"),
            username2=self.generate_username("bot"),
            username3=self.generate_username("bot"),
            message=random.choice([
                "GOVERNMENT HIDING TRUTH",
                "MEDIA LIES EXPOSED", 
                "CONSPIRACY REVEALED",
                "CORRUPTION EXPOSED"
            ]),
            content=random.choice([
                "SECRET DOCUMENTS LEAKED",
                "HIDDEN AGENDA EXPOSED",
                "TRUTH ABOUT POLITICIANS",
                "REAL FACTS REVEALED"
            ]),
            news=random.choice([
                "PM SECRET MEETING",
                "MINISTER SCANDAL",
                "ELECTION FRAUD",
                "MEDIA BLACKOUT"
            ]),
            statement=random.choice([
                "Elections are rigged",
                "Media controlled by government",
                "Opposition is fake",
                "People being fooled"
            ])
        )
        
        return content
    
    def _detect_language(self, content: str) -> str:
        """Simple language detection"""
        hindi_chars = sum(1 for char in content if '\u0900' <= char <= '\u097F')
        if hindi_chars > len(content) * 0.3:
            return "hindi"
        elif hindi_chars > 0:
            return "mixed"
        else:
            return "english"
    
    def _generate_engagement_metrics(self, user_profile: Dict[str, Any], 
                                   content_type: str) -> Dict[str, int]:
        """Generate realistic engagement metrics"""
        user_type = user_profile.get("user_type", "normal")
        followers = user_profile.get("followers_count", 100)
        
        # Base engagement rates
        if user_type == "bot":
            # Bots have artificial engagement
            engagement_rate = random.uniform(0.15, 0.35)  # Higher than normal
            likes = int(followers * engagement_rate * random.uniform(0.8, 1.2))
            # Bots get fewer genuine comments
            comments = max(1, int(likes * random.uniform(0.05, 0.15)))
            shares = max(0, int(likes * random.uniform(0.1, 0.3)))  # Bots share a lot
        elif content_type == "high_risk":
            # Controversial content gets mixed engagement
            engagement_rate = random.uniform(0.02, 0.08)
            likes = int(followers * engagement_rate)
            comments = max(0, int(likes * random.uniform(0.2, 0.5)))  # More comments on controversial
            shares = max(0, int(likes * random.uniform(0.05, 0.15)))
        else:
            # Normal engagement
            engagement_rate = random.uniform(0.01, 0.05)
            likes = int(followers * engagement_rate)
            comments = max(0, int(likes * random.uniform(0.1, 0.3)))
            shares = max(0, int(likes * random.uniform(0.02, 0.1)))
        
        return {
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "views": likes * random.randint(3, 10),
            "engagement_rate": round(engagement_rate * 100, 2)
        }
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        import re
        hashtags = re.findall(r'#\w+', content)
        return [tag.lower() for tag in hashtags]
    
    def _extract_mentions(self, content: str) -> List[str]:
        """Extract mentions from content"""
        import re
        mentions = re.findall(r'@\w+', content)
        return [mention[1:] for mention in mentions]  # Remove @ symbol
    
    def _generate_media_attachments(self) -> List[Dict[str, Any]]:
        """Generate media attachments"""
        if random.random() < 0.3:  # 30% chance of media
            media_types = ["image", "video", "document"]
            media_type = random.choice(media_types)
            
            return [{
                "type": media_type,
                "url": f"https://example.com/media/{uuid.uuid4()}.{media_type[:3]}",
                "size": random.randint(100000, 5000000),  # 100KB to 5MB
                "duration": random.randint(10, 300) if media_type == "video" else None
            }]
        return []
    
    def _generate_ip_metadata(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate IP and location metadata"""
        # Simulate Indian IP ranges
        indian_ip_ranges = [
            "103.{}.{}.{}",
            "117.{}.{}.{}",
            "182.{}.{}.{}",
            "49.{}.{}.{}",
            "14.{}.{}.{}"
        ]
        
        ip_template = random.choice(indian_ip_ranges)
        ip_address = ip_template.format(
            random.randint(1, 255),
            random.randint(1, 255),
            random.randint(1, 255)
        )
        
        return {
            "ip_address": ip_address,
            "country": "India",
            "state": random.choice([
                "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Gujarat",
                "Rajasthan", "Uttar Pradesh", "West Bengal", "Punjab", "Haryana"
            ]),
            "city": user_profile["location"],
            "isp": random.choice([
                "Jio", "Airtel", "Vi", "BSNL", "ACT Fibernet", "Hathway"
            ]),
            "is_vpn": random.random() < 0.1,  # 10% VPN usage
            "is_tor": random.random() < 0.02   # 2% Tor usage
        }
    
    def _generate_device_info(self) -> Dict[str, Any]:
        """Generate device information"""
        devices = [
            {"type": "mobile", "os": "Android", "browser": "Chrome Mobile"},
            {"type": "mobile", "os": "iOS", "browser": "Safari Mobile"},
            {"type": "desktop", "os": "Windows", "browser": "Chrome"},
            {"type": "desktop", "os": "macOS", "browser": "Safari"},
            {"type": "tablet", "os": "Android", "browser": "Chrome"}
        ]
        
        device = random.choice(devices)
        
        return {
            "device_type": device["type"],
            "operating_system": device["os"],
            "browser": device["browser"],
            "user_agent": f"Mozilla/5.0 ({device['os']}) {device['browser']}/91.0",
            "screen_resolution": random.choice([
                "1920x1080", "1366x768", "414x896", "375x667", "768x1024"
            ]),
            "timezone": "Asia/Kolkata"
        }
    
    def _analyze_threat_indicators(self, content: str, content_type: str) -> Dict[str, Any]:
        """Analyze threat indicators in content"""
        indicators = {
            "terrorism_keywords": [],
            "anti_national_keywords": [],
            "cybercrime_keywords": [],
            "bot_indicators": [],
            "coordination_signals": [],
            "urgency_markers": [],
            "violence_indicators": []
        }
        
        content_lower = content.lower()
        
        # Check for various threat indicators
        for keyword in self.terrorism_keywords:
            if keyword in content_lower:
                indicators["terrorism_keywords"].append(keyword)
        
        for keyword in self.anti_national_keywords:
            if keyword in content_lower:
                indicators["anti_national_keywords"].append(keyword)
        
        for keyword in self.cybercrime_keywords:
            if keyword in content_lower:
                indicators["cybercrime_keywords"].append(keyword)
        
        # Bot indicators
        if content.count("!!!") > 2:
            indicators["bot_indicators"].append("excessive_exclamation")
        
        if content.count("Follow @") > 1:
            indicators["bot_indicators"].append("multiple_follow_requests")
        
        if any(word in content_lower for word in ["urgent", "breaking", "alert"]):
            indicators["urgency_markers"].append("urgency_language")
        
        # Violence indicators
        if any(word in content_lower for word in ["kill", "destroy", "attack", "bomb"]):
            indicators["violence_indicators"].append("violent_language")
        
        return indicators

    def generate_coordinated_campaign(self, campaign_type: str = "anti_national",
                                    num_accounts: int = 20, 
                                    num_posts: int = 100) -> Dict[str, Any]:
        """Generate a coordinated bot campaign"""
        
        campaign_themes = {
            "anti_national": {
                "hashtags": ["#FreeKashmir", "#BreakIndia", "#PakistanZindabad"],
                "keywords": self.anti_national_keywords,
                "content_template": "भारत के खिलाफ {action}! {location} needs {goal}! {hashtag}"
            },
            "terrorism": {
                "hashtags": ["#Jihad", "#IslamicState", "#RevolutionNow"],
                "keywords": self.terrorism_keywords,
                "content_template": "Time for {action} against {target}! Join the {movement}! {hashtag}"
            },
            "cybercrime": {
                "hashtags": ["#CryptoDeals", "#HackingServices", "#DataForSale"],
                "keywords": self.cybercrime_keywords,
                "content_template": "Selling {product}! Payment in {crypto}! Contact {contact}! {hashtag}"
            }
        }
        
        theme = campaign_themes.get(campaign_type, campaign_themes["anti_national"])
        
        # Generate coordinated accounts
        accounts = []
        for i in range(num_accounts):
            profile = self.generate_user_profile("bot")
            profile["campaign_id"] = f"CAMP_{campaign_type.upper()}_{uuid.uuid4().hex[:8]}"
            profile["coordination_role"] = random.choice(["amplifier", "content_creator", "influencer"])
            accounts.append(profile)
        
        # Generate coordinated posts
        posts = []
        campaign_hashtag = random.choice(theme["hashtags"])
        
        for i in range(num_posts):
            account = random.choice(accounts)
            
            # Create similar content with variations
            base_content = theme["content_template"].format(
                action=random.choice(["प्रदर्शन करते हैं", "आवाज उठाते हैं", "संघर्ष करते हैं"]),
                location=random.choice(["Kashmir", "Punjab", "Northeast"]),
                goal=random.choice(["freedom", "azadi", "independence"]),
                target=random.choice(["government", "system", "oppression"]),
                movement=random.choice(["revolution", "resistance", "uprising"]),
                product=random.choice(["bank data", "credit cards", "hacking tools"]),
                crypto=random.choice(["Bitcoin", "Ethereum", "Monero"]),
                contact=f"@{self.generate_username('bot')}",
                hashtag=campaign_hashtag
            )
            
            post = self.generate_social_media_post(account, "high_risk")
            post["content"] = base_content
            post["campaign_id"] = account["campaign_id"]
            post["coordination_score"] = random.uniform(0.7, 0.95)
            
            # Add timing coordination (posts within similar time windows)
            base_time = datetime.now() - timedelta(hours=random.randint(1, 48))
            coordination_window = random.randint(-30, 30)  # Within 30 minutes of each other
            post["timestamp"] = (base_time + timedelta(minutes=coordination_window)).isoformat()
            
            posts.append(post)
        
        return {
            "campaign_id": f"CAMP_{campaign_type.upper()}_{uuid.uuid4().hex[:8]}",
            "campaign_type": campaign_type,
            "accounts": accounts,
            "posts": posts,
            "coordination_metrics": {
                "similarity_score": random.uniform(0.8, 0.95),
                "temporal_clustering": random.uniform(0.7, 0.9),
                "hashtag_coordination": random.uniform(0.85, 0.98),
                "network_density": random.uniform(0.6, 0.8),
                "automated_behavior_score": random.uniform(0.75, 0.92)
            },
            "detection_difficulty": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "threat_level": random.choice(["MEDIUM", "HIGH", "CRITICAL"]),
            "geographic_spread": random.sample(self.indian_cities, k=random.randint(3, 8))
        }
    
    def generate_user_network(self, num_users: int = 100) -> Dict[str, Any]:
        """Generate a network of connected users with suspicious connections"""
        
        users = []
        connections = []
        
        # Generate users with different risk levels
        risk_distribution = {
            "low": 0.7,      # 70% normal users
            "medium": 0.2,   # 20% suspicious users  
            "high": 0.1      # 10% high-risk users
        }
        
        for i in range(num_users):
            rand = random.random()
            if rand < risk_distribution["low"]:
                user_type = "normal"
            elif rand < risk_distribution["low"] + risk_distribution["medium"]:
                user_type = "suspicious"
            else:
                user_type = "bot"
            
            user = self.generate_user_profile(user_type)
            user["network_id"] = f"NET_{i:04d}"
            users.append(user)
        
        # Generate connections
        for i, user in enumerate(users):
            # Number of connections based on user type
            if user["user_type"] == "bot":
                num_connections = random.randint(10, 50)  # Bots connect to many
            elif user["user_type"] == "suspicious":
                num_connections = random.randint(5, 20)   # Moderate connections
            else:
                num_connections = random.randint(1, 10)   # Normal connections
            
            # Create connections
            for _ in range(min(num_connections, len(users) - 1)):
                target_user = random.choice([u for u in users if u != user])
                
                connection = {
                    "from_user": user["user_id"],
                    "to_user": target_user["user_id"],
                    "connection_type": random.choice([
                        "follower", "following", "mutual", "mentioned", "replied"
                    ]),
                    "connection_strength": random.uniform(0.1, 1.0),
                    "first_interaction": (datetime.now() - timedelta(
                        days=random.randint(1, 365))).isoformat(),
                    "interaction_frequency": random.choice([
                        "daily", "weekly", "monthly", "rare", "one-time"
                    ]),
                    "suspicious_indicators": self._analyze_connection_suspicion(user, target_user)
                }
                
                connections.append(connection)
        
        # Identify suspicious clusters
        suspicious_clusters = self._identify_suspicious_clusters(users, connections)
        
        return {
            "network_id": f"NETWORK_{uuid.uuid4().hex[:8]}",
            "users": users,
            "connections": connections,
            "network_metrics": {
                "total_users": len(users),
                "total_connections": len(connections),
                "average_connections_per_user": len(connections) / len(users),
                "suspicious_clusters": len(suspicious_clusters),
                "bot_percentage": len([u for u in users if u["user_type"] == "bot"]) / len(users) * 100,
                "risk_score": sum(u["risk_score"] for u in users) / len(users)
            },
            "suspicious_clusters": suspicious_clusters,
            "geographic_distribution": self._analyze_geographic_distribution(users),
            "temporal_patterns": self._analyze_temporal_patterns(users)
        }
    
    def _analyze_connection_suspicion(self, user1: Dict, user2: Dict) -> List[str]:
        """Analyze suspicious indicators in connections"""
        indicators = []
        
        # Same location but different backgrounds
        if user1["location"] == user2["location"]:
            if user1["user_type"] != user2["user_type"]:
                indicators.append("location_risk_mismatch")
        
        # Both high-risk users
        if user1["risk_score"] > 50 and user2["risk_score"] > 50:
            indicators.append("high_risk_connection")
        
        # Bot connecting to suspicious user
        if (user1["user_type"] == "bot" and user2["user_type"] == "suspicious") or \
           (user1["user_type"] == "suspicious" and user2["user_type"] == "bot"):
            indicators.append("bot_suspicious_link")
        
        # Account creation timing
        if abs((datetime.fromisoformat(user1["account_created"]) - 
               datetime.fromisoformat(user2["account_created"])).days) < 7:
            indicators.append("simultaneous_account_creation")
        
        return indicators
    
    def _identify_suspicious_clusters(self, users: List[Dict], 
                                    connections: List[Dict]) -> List[Dict[str, Any]]:
        """Identify clusters of suspicious users"""
        clusters = []
        
        # Find groups of connected high-risk users
        high_risk_users = [u for u in users if u["risk_score"] > 60]
        
        for i in range(min(3, len(high_risk_users) // 5)):  # Max 3 clusters
            cluster_size = random.randint(3, 8)
            cluster_users = random.sample(high_risk_users, 
                                        min(cluster_size, len(high_risk_users)))
            
            cluster = {
                "cluster_id": f"CLUSTER_{i+1}",
                "users": [u["user_id"] for u in cluster_users],
                "cluster_type": random.choice([
                    "terrorism_cell", "bot_network", "coordination_group"
                ]),
                "risk_level": "HIGH",
                "activity_pattern": random.choice([
                    "synchronized", "coordinated", "distributed"
                ]),
                "geographic_concentration": len(set(u["location"] for u in cluster_users)) <= 2,
                "threat_indicators": [
                    "coordinated_posting",
                    "similar_content_patterns", 
                    "synchronized_timing",
                    "cross_platform_presence"
                ]
            }
            
            clusters.append(cluster)
        
        return clusters
    
    def _analyze_geographic_distribution(self, users: List[Dict]) -> Dict[str, Any]:
        """Analyze geographic distribution of users"""
        location_counts = {}
        risk_by_location = {}
        
        for user in users:
            location = user["location"]
            location_counts[location] = location_counts.get(location, 0) + 1
            
            if location not in risk_by_location:
                risk_by_location[location] = []
            risk_by_location[location].append(user["risk_score"])
        
        # Calculate average risk by location
        location_risk_avg = {
            loc: sum(scores) / len(scores) 
            for loc, scores in risk_by_location.items()
        }
        
        # Identify high-risk locations
        high_risk_locations = [
            loc for loc, avg_risk in location_risk_avg.items() 
            if avg_risk > 40
        ]
        
        return {
            "total_locations": len(location_counts),
            "user_distribution": location_counts,
            "average_risk_by_location": location_risk_avg,
            "high_risk_locations": high_risk_locations,
            "geographic_concentration": max(location_counts.values()) / len(users)
        }
    
    def _analyze_temporal_patterns(self, users: List[Dict]) -> Dict[str, Any]:
        """Analyze temporal patterns in user activities"""
        account_creation_dates = [
            datetime.fromisoformat(u["account_created"]) for u in users
        ]
        
        # Find creation clusters (accounts created within short time periods)
        creation_clusters = []
        sorted_dates = sorted(account_creation_dates)
        
        current_cluster = [sorted_dates[0]]
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - sorted_dates[i-1]).days <= 7:  # Within a week
                current_cluster.append(sorted_dates[i])
            else:
                if len(current_cluster) >= 3:  # Cluster of 3+ accounts
                    creation_clusters.append(current_cluster)
                current_cluster = [sorted_dates[i]]
        
        if len(current_cluster) >= 3:
            creation_clusters.append(current_cluster)
        
        return {
            "account_creation_span": (max(account_creation_dates) - min(account_creation_dates)).days,
            "creation_clusters": len(creation_clusters),
            "suspicious_timing_groups": [
                {
                    "start_date": min(cluster).isoformat(),
                    "end_date": max(cluster).isoformat(),
                    "account_count": len(cluster)
                }
                for cluster in creation_clusters
            ],
            "recent_account_percentage": len([
                d for d in account_creation_dates 
                if (datetime.now() - d).days <= 30
            ]) / len(users) * 100
        }
    
    def generate_trending_data(self) -> Dict[str, Any]:
        """Generate trending keywords, hashtags, and patterns"""
        
        # Generate trending hashtags
        trending_hashtags = []
        
        # Normal trending topics
        normal_trends = [
            {"tag": "#IPL2025", "volume": random.randint(50000, 200000), "sentiment": "positive"},
            {"tag": "#Bollywood", "volume": random.randint(30000, 100000), "sentiment": "mixed"},
            {"tag": "#IndianFood", "volume": random.randint(20000, 80000), "sentiment": "positive"},
            {"tag": "#MondayMotivation", "volume": random.randint(10000, 50000), "sentiment": "positive"},
            {"tag": "#WeatherUpdate", "volume": random.randint(15000, 60000), "sentiment": "neutral"}
        ]
        
        # Suspicious trends
        suspicious_trends = [
            {"tag": "#FreeKashmir", "volume": random.randint(5000, 25000), "sentiment": "negative"},
            {"tag": "#GovernmentFailed", "volume": random.randint(3000, 15000), "sentiment": "negative"},
            {"tag": "#RevolutionNow", "volume": random.randint(2000, 10000), "sentiment": "aggressive"},
            {"tag": "#TruthExposed", "volume": random.randint(4000, 20000), "sentiment": "controversial"}
        ]
        
        trending_hashtags.extend(normal_trends)
        trending_hashtags.extend(suspicious_trends)
        
        # Generate trending keywords
        trending_keywords = [
            {"keyword": "election fraud", "spike_factor": 3.5, "risk_level": "HIGH"},
            {"keyword": "government conspiracy", "spike_factor": 2.8, "risk_level": "MEDIUM"},
            {"keyword": "media blackout", "spike_factor": 2.2, "risk_level": "MEDIUM"},
            {"keyword": "bitcoin scam", "spike_factor": 4.1, "risk_level": "HIGH"},
            {"keyword": "hack bank account", "spike_factor": 3.9, "risk_level": "CRITICAL"},
            {"keyword": "bomb threat", "spike_factor": 5.0, "risk_level": "CRITICAL"},
            {"keyword": "anti national", "spike_factor": 2.7, "risk_level": "HIGH"}
        ]
        
        # Geographic trends
        geographic_trends = {}
        for city in random.sample(self.indian_cities, 10):
            geographic_trends[city] = {
                "trending_topics": random.sample([t["tag"] for t in trending_hashtags], 3),
                "threat_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "activity_volume": random.randint(1000, 50000),
                "suspicious_activity_percentage": random.uniform(5, 25)
            }
        
        # Temporal trends
        hourly_patterns = {}
        for hour in range(24):
            hourly_patterns[f"{hour:02d}:00"] = {
                "total_posts": random.randint(1000, 10000),
                "suspicious_posts": random.randint(50, 500),
                "bot_activity": random.randint(20, 200),
                "peak_activity": hour in [9, 12, 18, 21]  # Peak hours
            }
        
        return {
            "trending_hashtags": sorted(trending_hashtags, key=lambda x: x["volume"], reverse=True),
            "trending_keywords": sorted(trending_keywords, key=lambda x: x["spike_factor"], reverse=True),
            "geographic_trends": geographic_trends,
            "temporal_patterns": {
                "hourly_activity": hourly_patterns,
                "peak_hours": [9, 12, 18, 21],
                "suspicious_activity_peaks": [2, 15, 22],  # Late night, afternoon, night
                "bot_activity_peaks": [3, 14, 23]
            },
            "platform_distribution": {
                "Twitter": random.randint(30000, 100000),
                "Facebook": random.randint(50000, 150000),
                "Instagram": random.randint(25000, 80000),
                "Telegram": random.randint(10000, 40000),
                "WhatsApp": random.randint(40000, 120000)
            },
            "alert_triggers": [
                {
                    "keyword": "bomb",
                    "threshold_reached": True,
                    "current_mentions": 347,
                    "normal_baseline": 12,
                    "spike_factor": 28.9
                },
                {
                    "keyword": "government conspiracy",
                    "threshold_reached": True,
                    "current_mentions": 1289,
                    "normal_baseline": 156,
                    "spike_factor": 8.3
                }
            ]
        }
    
    def generate_complete_dataset(self, num_posts: int = 500) -> Dict[str, Any]:
        """Generate a complete dataset for demonstration"""
        
        print("🔄 Generating comprehensive police AI monitoring dataset...")
        
        # Generate user base
        print("👥 Creating user profiles...")
        users = []
        
        # Distribution: 70% normal, 20% suspicious, 10% bots
        for i in range(100):  # Generate 100 users
            if i < 70:
                user_type = "normal"
            elif i < 90:
                user_type = "suspicious" 
            else:
                user_type = "bot"
                
            user = self.generate_user_profile(user_type)
            users.append(user)
        
        # Generate posts
        print("📝 Generating social media posts...")
        posts = []
        
        for i in range(num_posts):
            # Content type distribution
            if i < num_posts * 0.6:  # 60% normal
                content_type = "normal"
            elif i < num_posts * 0.8:  # 20% suspicious
                content_type = "suspicious"
            elif i < num_posts * 0.9:  # 10% high risk
                content_type = "high_risk"
            else:  # 10% bot content
                content_type = "bot"
            
            user = random.choice(users)
            post = self.generate_social_media_post(user, content_type)
            posts.append(post)
        
        # Generate coordinated campaigns
        print("🕸️ Creating coordinated campaigns...")
        campaigns = [
            self.generate_coordinated_campaign("anti_national", 15, 30),
            self.generate_coordinated_campaign("terrorism", 10, 20),
            self.generate_coordinated_campaign("cybercrime", 12, 25)
        ]
        
        # Generate user network
        print("🌐 Building user networks...")
        network = self.generate_user_network(100)
        
        # Generate trending data
        print("📈 Analyzing trends...")
        trends = self.generate_trending_data()
        
        # Compile complete dataset
        dataset = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "dataset_version": "1.0",
                "total_users": len(users),
                "total_posts": len(posts),
                "total_campaigns": len(campaigns),
                "geographic_coverage": len(set(u["location"] for u in users)),
                "time_span_days": 30,
                "languages": ["hindi", "english", "mixed"]
            },
            "users": users,
            "posts": posts,
            "coordinated_campaigns": campaigns,
            "user_networks": network,
            "trending_analysis": trends,
            "summary_statistics": {
                "threat_distribution": {
                    "low_risk": len([p for p in posts if p["risk_score"] < 25]),
                    "medium_risk": len([p for p in posts if 25 <= p["risk_score"] < 60]),
                    "high_risk": len([p for p in posts if p["risk_score"] >= 60])
                },
                "platform_distribution": {
                    platform: len([p for p in posts if p["platform"] == platform])
                    for platform in self.platforms
                },
                "language_distribution": {
                    "hindi": len([p for p in posts if p["language"] == "hindi"]),
                    "english": len([p for p in posts if p["language"] == "english"]), 
                    "mixed": len([p for p in posts if p["language"] == "mixed"])
                },
                "geographic_hotspots": sorted(
                    {city: len([p for p in posts if p["location"] == city]) 
                     for city in set(p["location"] for p in posts)}.items(),
                    key=lambda x: x[1], reverse=True
                )[:10]
            }
        }
        
        print("✅ Dataset generation complete!")
        return dataset
