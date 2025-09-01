"""
Advanced Bot Profile Generator for Police AI Monitoring
Creates sophisticated bot profiles with realistic behavioral patterns
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple

class BotProfileGenerator:
    """Generate sophisticated bot profiles for testing detection algorithms"""
    
    def __init__(self):
        # Bot naming patterns
        self.bot_naming_patterns = {
            "simple": [
                "{first_name}{numbers}",
                "{first_name}_{numbers}",
                "{adjective}{first_name}",
                "real_{first_name}",
                "official_{first_name}"
            ],
            "sophisticated": [
                "{first_name}.{last_name}{year}",
                "{first_name}_{location}_{numbers}",
                "{profession}_{first_name}",
                "{first_name}_{hobby}_lover"
            ],
            "government_impersonation": [
                "official_{department}",
                "govt_{office}_{city}",
                "min_{ministry}_{state}",
                "police_{city}_{numbers}",
                "sec_{department}_off"
            ]
        }
        
        # Bot behavioral patterns
        self.bot_behaviors = {
            "amplifier": {
                "posting_frequency": "very_high",  # 50+ posts/day
                "content_originality": 0.1,        # 90% reposts
                "engagement_pattern": "artificial", # Likes/shares without reading
                "response_time": "instant",         # <1 minute responses
                "activity_schedule": "24x7",        # Round-the-clock activity
                "language_quality": "poor",         # Grammar/spelling errors
                "topic_consistency": "single_focus" # Only one topic
            },
            "content_creator": {
                "posting_frequency": "high",        # 20-30 posts/day
                "content_originality": 0.3,        # 30% original content
                "engagement_pattern": "selective",  # Strategic engagement
                "response_time": "quick",           # 1-5 minute responses
                "activity_schedule": "peak_hours",  # Active during peak times
                "language_quality": "mixed",        # Variable quality
                "topic_consistency": "focused"      # 2-3 related topics
            },
            "influencer_bot": {
                "posting_frequency": "moderate",    # 10-15 posts/day
                "content_originality": 0.6,        # 60% original content
                "engagement_pattern": "strategic",  # Calculated interactions
                "response_time": "delayed",         # 5-30 minute responses
                "activity_schedule": "human_like",  # Mimics human patterns
                "language_quality": "good",         # Better language use
                "topic_consistency": "diverse"      # Multiple topics
            },
            "sleeper_agent": {
                "posting_frequency": "low",         # 2-5 posts/day
                "content_originality": 0.8,        # Mostly original content
                "engagement_pattern": "organic",    # Natural-seeming engagement
                "response_time": "human",           # Variable response times
                "activity_schedule": "irregular",   # Sporadic activity
                "language_quality": "excellent",    # High-quality language
                "topic_consistency": "normal"       # Normal topic range
            }
        }
        
        # Sophisticated evasion techniques
        self.evasion_techniques = {
            "content_manipulation": [
                "character_substitution",   # Using similar-looking characters
                "zero_width_characters",    # Invisible characters
                "text_spacing",             # Unusual spacing patterns
                "emoji_encoding",           # Hiding meaning in emojis
                "language_mixing",          # Mixing scripts/languages
                "typo_injection"            # Intentional typos
            ],
            "timing_manipulation": [
                "human_schedule_mimicking", # Following human patterns
                "timezone_hopping",         # Posting from different timezones
                "delay_injection",          # Random delays between actions
                "burst_posting",            # Periods of high activity
                "dormant_periods"           # Periods of inactivity
            ],
            "network_evasion": [
                "ip_rotation",              # Changing IP addresses
                "device_spoofing",          # Fake device fingerprints
                "proxy_chains",             # Multiple proxy layers
                "residential_ips",          # Using residential IP ranges
                "mobile_rotation"           # Rotating mobile IPs
            ],
            "behavioral_mimicking": [
                "human_error_simulation",   # Simulating human mistakes
                "emotional_variance",       # Showing emotional responses
                "context_awareness",        # Responding to current events
                "personal_history",         # Maintaining consistent backstory
                "relationship_building"     # Building genuine connections
            ]
        }
        
        # Bot coordination strategies
        self.coordination_strategies = {
            "hashtag_campaigns": {
                "synchronization": "high",
                "variation": "low",
                "timing_window": 5,  # minutes
                "content_similarity": 0.8
            },
            "narrative_pushing": {
                "synchronization": "medium",
                "variation": "medium",
                "timing_window": 60,  # minutes
                "content_similarity": 0.6
            },
            "artificial_trends": {
                "synchronization": "very_high",
                "variation": "very_low",
                "timing_window": 2,  # minutes
                "content_similarity": 0.95
            },
            "reputation_attacks": {
                "synchronization": "high",
                "variation": "medium",
                "timing_window": 15,  # minutes
                "content_similarity": 0.7
            }
        }
    
    def generate_bot_profile(self, bot_type: str = "amplifier", 
                           sophistication: str = "medium") -> Dict[str, Any]:
        """Generate a comprehensive bot profile"""
        
        # Generate basic profile
        profile = self._generate_basic_bot_profile(bot_type, sophistication)
        
        # Add behavioral patterns
        profile["behavioral_patterns"] = self._generate_behavioral_patterns(bot_type)
        
        # Add evasion techniques
        profile["evasion_techniques"] = self._select_evasion_techniques(sophistication)
        
        # Add coordination capabilities
        profile["coordination_capabilities"] = self._generate_coordination_capabilities(bot_type)
        
        # Add technical fingerprints
        profile["technical_fingerprints"] = self._generate_technical_fingerprints(sophistication)
        
        # Add detection resistance metrics
        profile["detection_resistance"] = self._calculate_detection_resistance(profile)
        
        return profile
    
    def _generate_basic_bot_profile(self, bot_type: str, sophistication: str) -> Dict[str, Any]:
        """Generate basic bot profile information"""
        
        # Select naming pattern based on sophistication
        if sophistication == "low":
            pattern_type = "simple"
        elif sophistication == "high":
            pattern_type = random.choice(["sophisticated", "government_impersonation"])
        else:
            pattern_type = random.choice(["simple", "sophisticated"])
        
        # Generate username
        pattern = random.choice(self.bot_naming_patterns[pattern_type])
        username = self._fill_naming_pattern(pattern)
        
        # Account characteristics based on bot type
        if bot_type == "amplifier":
            followers = random.randint(100, 1000)
            following = random.randint(500, 5000)  # Follow many accounts
            posts_count = random.randint(1000, 10000)
            account_age_days = random.randint(30, 365)
        elif bot_type == "content_creator":
            followers = random.randint(500, 5000)
            following = random.randint(200, 1000)
            posts_count = random.randint(2000, 15000)
            account_age_days = random.randint(90, 730)
        elif bot_type == "influencer_bot":
            followers = random.randint(2000, 50000)
            following = random.randint(100, 500)
            posts_count = random.randint(1000, 8000)
            account_age_days = random.randint(180, 1095)
        else:  # sleeper_agent
            followers = random.randint(50, 500)
            following = random.randint(50, 300)
            posts_count = random.randint(100, 1000)
            account_age_days = random.randint(365, 1825)  # Older accounts
        
        return {
            "bot_id": str(uuid.uuid4()),
            "username": username,
            "display_name": self._generate_display_name(sophistication),
            "bio": self._generate_bot_bio(bot_type, sophistication),
            "bot_type": bot_type,
            "sophistication_level": sophistication,
            "followers_count": followers,
            "following_count": following,
            "posts_count": posts_count,
            "account_created": (datetime.now() - timedelta(days=account_age_days)).isoformat(),
            "verification_status": self._determine_verification_status(sophistication),
            "profile_completeness": self._calculate_profile_completeness(sophistication),
            "activity_score": self._calculate_activity_score(bot_type),
            "authenticity_indicators": self._generate_authenticity_indicators(sophistication)
        }
    
    def _fill_naming_pattern(self, pattern: str) -> str:
        """Fill naming pattern with realistic data"""
        
        indian_names = ["Raj", "Priya", "Amit", "Neha", "Vikram", "Anjali", "Rohit", "Kavya"]
        indian_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Pune"]
        adjectives = ["real", "official", "verified", "true", "news", "update"]
        professions = ["doctor", "engineer", "teacher", "journalist", "analyst"]
        departments = ["home", "finance", "defense", "external", "railways"]
        ministries = ["education", "health", "agriculture", "commerce", "labour"]
        
        return pattern.format(
            first_name=random.choice(indian_names).lower(),
            last_name=random.choice(["sharma", "patel", "singh", "kumar", "gupta"]),
            numbers=random.randint(100, 9999),
            year=random.randint(80, 99),
            location=random.choice(indian_cities).lower(),
            adjective=random.choice(adjectives),
            profession=random.choice(professions),
            hobby=random.choice(["cricket", "music", "travel", "food", "fitness"]),
            department=random.choice(departments),
            office=random.choice(["office", "dept", "min", "sec"]),
            city=random.choice(indian_cities).lower(),
            ministry=random.choice(ministries),
            state=random.choice(["mh", "dl", "ka", "tn", "gj"])
        )
    
    def _generate_display_name(self, sophistication: str) -> str:
        """Generate display name based on sophistication"""
        
        first_names = ["Rajesh", "Priya", "Amit", "Neha", "Vikram", "Anjali"]
        last_names = ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Agarwal"]
        
        if sophistication == "low":
            # Simple or obvious fake names
            return random.choice([
                f"{random.choice(first_names)} {random.choice(last_names)}",
                f"{random.choice(first_names)} {random.randint(100, 999)}",
                f"Real {random.choice(first_names)}",
                f"Official {random.choice(first_names)}"
            ])
        elif sophistication == "high":
            # More realistic names with titles
            titles = ["Dr.", "Prof.", "Mr.", "Ms.", ""]
            return f"{random.choice(titles)} {random.choice(first_names)} {random.choice(last_names)}"
        else:
            # Medium sophistication
            return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_bot_bio(self, bot_type: str, sophistication: str) -> str:
        """Generate bot bio based on type and sophistication"""
        
        if sophistication == "low":
            bios = [
                "Breaking news and updates",
                "Real information only",
                "Truth seeker",
                "News updates 24/7",
                "Official account"
            ]
        elif sophistication == "high":
            if bot_type == "sleeper_agent":
                bios = [
                    "Software Engineer at TechCorp | Cricket enthusiast | Mumbai",
                    "Teacher | Book lover | Helping students succeed | Delhi",
                    "Doctor | Saving lives | Family person | Bangalore",
                    "Journalist | Uncovering truth | Independent media | Chennai"
                ]
            else:
                bios = [
                    "Digital Marketing Expert | Helping businesses grow online",
                    "Political Analyst | Commentary on current affairs | Views personal",
                    "Social Activist | Fighting for justice | Voice of the people",
                    "Technology Blogger | Latest tech news and reviews"
                ]
        else:  # medium
            bios = [
                "News enthusiast | Sharing important updates",
                "Proud Indian | Supporting good governance",
                "Information sharing | Stay informed",
                "Current affairs | Politics | Social issues"
            ]
        
        return random.choice(bios)
    
    def _determine_verification_status(self, sophistication: str) -> Dict[str, Any]:
        """Determine verification status and authenticity"""
        
        if sophistication == "high":
            # High sophistication bots might have fake verification
            fake_verification_chance = 0.15
        else:
            fake_verification_chance = 0.05
        
        return {
            "is_verified": random.random() < fake_verification_chance,
            "verification_type": random.choice(["blue_tick", "government", "media", "none"]),
            "verification_authenticity": "fake" if random.random() < 0.8 else "authentic"
        }
    
    def _calculate_profile_completeness(self, sophistication: str) -> float:
        """Calculate how complete the profile appears"""
        
        if sophistication == "low":
            return random.uniform(0.2, 0.5)  # Incomplete profiles
        elif sophistication == "high":
            return random.uniform(0.8, 1.0)  # Very complete profiles
        else:
            return random.uniform(0.5, 0.8)  # Moderately complete
    
    def _calculate_activity_score(self, bot_type: str) -> float:
        """Calculate activity score based on bot type"""
        
        activity_ranges = {
            "amplifier": (0.8, 1.0),      # Very high activity
            "content_creator": (0.6, 0.9), # High activity
            "influencer_bot": (0.4, 0.7),  # Moderate activity
            "sleeper_agent": (0.1, 0.4)    # Low activity
        }
        
        min_score, max_score = activity_ranges.get(bot_type, (0.3, 0.7))
        return random.uniform(min_score, max_score)
    
    def _generate_authenticity_indicators(self, sophistication: str) -> Dict[str, Any]:
        """Generate authenticity indicators"""
        
        if sophistication == "low":
            return {
                "profile_photo": "generic_or_stolen",
                "bio_quality": "poor",
                "posting_patterns": "robotic",
                "interaction_quality": "artificial",
                "content_originality": "low",
                "language_consistency": "poor"
            }
        elif sophistication == "high":
            return {
                "profile_photo": "realistic_or_ai_generated",
                "bio_quality": "good",
                "posting_patterns": "human_like",
                "interaction_quality": "natural",
                "content_originality": "mixed",
                "language_consistency": "good"
            }
        else:
            return {
                "profile_photo": "stock_photo",
                "bio_quality": "moderate",
                "posting_patterns": "somewhat_robotic",
                "interaction_quality": "mixed",
                "content_originality": "low_to_moderate",
                "language_consistency": "inconsistent"
            }
    
    def _generate_behavioral_patterns(self, bot_type: str) -> Dict[str, Any]:
        """Generate detailed behavioral patterns"""
        
        base_behavior = self.bot_behaviors[bot_type].copy()
        
        # Add specific metrics
        posting_frequency_map = {
            "very_high": random.randint(50, 200),  # posts per day
            "high": random.randint(20, 50),
            "moderate": random.randint(10, 20),
            "low": random.randint(2, 10)
        }
        
        response_time_map = {
            "instant": random.uniform(0.1, 1.0),   # minutes
            "quick": random.uniform(1.0, 5.0),
            "delayed": random.uniform(5.0, 30.0),
            "human": random.uniform(10.0, 120.0)
        }
        
        base_behavior["posts_per_day"] = posting_frequency_map[base_behavior["posting_frequency"]]
        base_behavior["avg_response_time_minutes"] = response_time_map[base_behavior["response_time"]]
        
        # Add activity schedule details
        if base_behavior["activity_schedule"] == "24x7":
            base_behavior["hourly_activity"] = [random.uniform(0.8, 1.0) for _ in range(24)]
        elif base_behavior["activity_schedule"] == "peak_hours":
            # Active during typical peak hours (9-12, 18-23)
            activity = []
            for hour in range(24):
                if hour in [9, 10, 11, 18, 19, 20, 21, 22]:
                    activity.append(random.uniform(0.7, 1.0))
                else:
                    activity.append(random.uniform(0.1, 0.4))
            base_behavior["hourly_activity"] = activity
        else:
            # More human-like patterns
            base_behavior["hourly_activity"] = [random.uniform(0.1, 0.8) for _ in range(24)]
        
        return base_behavior
    
    def _select_evasion_techniques(self, sophistication: str) -> List[str]:
        """Select evasion techniques based on sophistication"""
        
        all_techniques = []
        for category, techniques in self.evasion_techniques.items():
            all_techniques.extend(techniques)
        
        if sophistication == "low":
            # Use basic evasion techniques
            num_techniques = random.randint(1, 3)
            return random.sample(all_techniques[:8], min(num_techniques, 8))
        elif sophistication == "high":
            # Use advanced evasion techniques
            num_techniques = random.randint(5, 10)
            return random.sample(all_techniques, min(num_techniques, len(all_techniques)))
        else:
            # Use moderate evasion techniques
            num_techniques = random.randint(3, 6)
            return random.sample(all_techniques, min(num_techniques, len(all_techniques)))
    
    def _generate_coordination_capabilities(self, bot_type: str) -> Dict[str, Any]:
        """Generate coordination capabilities"""
        
        if bot_type == "amplifier":
            strategies = ["hashtag_campaigns", "artificial_trends"]
        elif bot_type == "content_creator":
            strategies = ["narrative_pushing", "hashtag_campaigns"]
        elif bot_type == "influencer_bot":
            strategies = ["narrative_pushing", "reputation_attacks"]
        else:  # sleeper_agent
            strategies = ["narrative_pushing"]
        
        selected_strategy = random.choice(strategies)
        strategy_config = self.coordination_strategies[selected_strategy].copy()
        
        return {
            "primary_strategy": selected_strategy,
            "coordination_config": strategy_config,
            "network_role": random.choice(["leader", "follower", "amplifier", "coordinator"]),
            "coordination_frequency": random.choice(["continuous", "scheduled", "event_triggered"]),
            "cross_platform": random.random() < 0.3  # 30% operate across platforms
        }
    
    def _generate_technical_fingerprints(self, sophistication: str) -> Dict[str, Any]:
        """Generate technical fingerprints for detection"""
        
        if sophistication == "low":
            # Obvious technical fingerprints
            return {
                "user_agent_consistency": False,
                "ip_address_patterns": "static_datacenter",
                "device_fingerprint_variation": "none",
                "browser_automation_traces": "obvious",
                "network_timing_patterns": "robotic",
                "session_management": "poor"
            }
        elif sophistication == "high":
            # Advanced fingerprint masking
            return {
                "user_agent_consistency": True,
                "ip_address_patterns": "residential_rotation",
                "device_fingerprint_variation": "realistic",
                "browser_automation_traces": "well_hidden",
                "network_timing_patterns": "human_like",
                "session_management": "sophisticated"
            }
        else:
            # Moderate fingerprint masking
            return {
                "user_agent_consistency": random.choice([True, False]),
                "ip_address_patterns": "basic_rotation",
                "device_fingerprint_variation": "limited",
                "browser_automation_traces": "partially_hidden",
                "network_timing_patterns": "somewhat_robotic",
                "session_management": "basic"
            }
    
    def _calculate_detection_resistance(self, profile: Dict[str, Any]) -> Dict[str, float]:
        """Calculate how resistant the bot is to detection"""
        
        sophistication = profile["sophistication_level"]
        bot_type = profile["bot_type"]
        
        # Base resistance scores
        if sophistication == "low":
            base_resistance = 0.2
        elif sophistication == "high":
            base_resistance = 0.8
        else:
            base_resistance = 0.5
        
        # Adjust based on bot type
        type_modifiers = {
            "amplifier": -0.1,      # Easier to detect due to high activity
            "content_creator": 0.0,  # Neutral
            "influencer_bot": 0.1,   # Harder to detect
            "sleeper_agent": 0.2     # Much harder to detect
        }
        
        adjusted_resistance = base_resistance + type_modifiers.get(bot_type, 0)
        
        # Calculate specific resistance metrics
        return {
            "overall_resistance": max(0.0, min(1.0, adjusted_resistance)),
            "behavioral_analysis_resistance": adjusted_resistance + random.uniform(-0.1, 0.1),
            "network_analysis_resistance": adjusted_resistance + random.uniform(-0.15, 0.15),
            "content_analysis_resistance": adjusted_resistance + random.uniform(-0.1, 0.1),
            "temporal_analysis_resistance": adjusted_resistance + random.uniform(-0.2, 0.2),
            "linguistic_analysis_resistance": adjusted_resistance + random.uniform(-0.1, 0.1)
        }
    
    def generate_bot_network(self, network_size: int = 50, 
                           coordination_level: str = "high") -> Dict[str, Any]:
        """Generate a coordinated bot network"""
        
        # Determine bot type distribution
        if coordination_level == "high":
            # Well-organized network
            type_distribution = {
                "amplifier": 0.6,       # 60% amplifiers
                "content_creator": 0.25, # 25% content creators
                "influencer_bot": 0.10,  # 10% influencers
                "sleeper_agent": 0.05    # 5% sleepers
            }
            sophistication_distribution = ["medium", "high"]
        elif coordination_level == "medium":
            # Moderately organized network
            type_distribution = {
                "amplifier": 0.7,
                "content_creator": 0.2,
                "influencer_bot": 0.08,
                "sleeper_agent": 0.02
            }
            sophistication_distribution = ["low", "medium", "high"]
        else:  # low coordination
            # Loosely organized network
            type_distribution = {
                "amplifier": 0.8,
                "content_creator": 0.15,
                "influencer_bot": 0.04,
                "sleeper_agent": 0.01
            }
            sophistication_distribution = ["low", "medium"]
        
        # Generate bots
        bots = []
        for i in range(network_size):
            # Select bot type based on distribution
            rand = random.random()
            cumulative = 0
            for bot_type, prob in type_distribution.items():
                cumulative += prob
                if rand <= cumulative:
                    selected_type = bot_type
                    break
            
            # Select sophistication
            sophistication = random.choice(sophistication_distribution)
            
            # Generate bot profile
            bot = self.generate_bot_profile(selected_type, sophistication)
            bot["network_id"] = f"NET_{uuid.uuid4().hex[:8]}"
            bot["network_role"] = self._assign_network_role(selected_type, i, network_size)
            
            bots.append(bot)
        
        # Generate network connections
        connections = self._generate_network_connections(bots, coordination_level)
        
        # Generate coordination schedule
        coordination_schedule = self._generate_coordination_schedule(coordination_level)
        
        return {
            "network_id": f"BOTNET_{uuid.uuid4().hex[:8]}",
            "coordination_level": coordination_level,
            "network_size": network_size,
            "bots": bots,
            "connections": connections,
            "coordination_schedule": coordination_schedule,
            "network_metrics": self._calculate_network_metrics(bots, connections),
            "detection_difficulty": self._assess_network_detection_difficulty(bots, coordination_level),
            "operational_objectives": self._generate_operational_objectives(coordination_level),
            "threat_assessment": self._assess_network_threat_level(bots, coordination_level)
        }
    
    def _assign_network_role(self, bot_type: str, index: int, total_size: int) -> str:
        """Assign network role based on bot type and position"""
        
        if index < total_size * 0.05:  # Top 5%
            return "commander"
        elif index < total_size * 0.15:  # Next 10%
            return "coordinator"
        elif bot_type == "influencer_bot":
            return "influence_node"
        elif bot_type == "content_creator":
            return "content_producer"
        elif bot_type == "sleeper_agent":
            return "sleeper"
        else:  # amplifier
            return "amplifier"
    
    def _generate_network_connections(self, bots: List[Dict], 
                                    coordination_level: str) -> List[Dict[str, Any]]:
        """Generate connections between bots in the network"""
        
        connections = []
        
        # Connection density based on coordination level
        if coordination_level == "high":
            connection_density = 0.3  # 30% of possible connections
        elif coordination_level == "medium":
            connection_density = 0.15  # 15% of possible connections
        else:
            connection_density = 0.08  # 8% of possible connections
        
        # Generate connections
        for i, bot1 in enumerate(bots):
            for j, bot2 in enumerate(bots[i+1:], i+1):
                if random.random() < connection_density:
                    connection = {
                        "from_bot": bot1["bot_id"],
                        "to_bot": bot2["bot_id"],
                        "connection_type": random.choice([
                            "follows", "amplifies", "coordinates", "receives_commands"
                        ]),
                        "connection_strength": random.uniform(0.3, 1.0),
                        "established_date": (datetime.now() - timedelta(
                            days=random.randint(1, 180))).isoformat(),
                        "interaction_frequency": random.choice([
                            "daily", "weekly", "event_triggered", "continuous"
                        ])
                    }
                    connections.append(connection)
        
        return connections
    
    def _generate_coordination_schedule(self, coordination_level: str) -> Dict[str, Any]:
        """Generate coordination schedule for the network"""
        
        if coordination_level == "high":
            return {
                "schedule_type": "synchronized",
                "coordination_windows": [
                    {"start": "09:00", "end": "12:00", "activity": "morning_campaign"},
                    {"start": "18:00", "end": "22:00", "activity": "evening_amplification"}
                ],
                "emergency_activation": "within_5_minutes",
                "content_synchronization": "real_time",
                "cross_platform_coordination": True
            }
        elif coordination_level == "medium":
            return {
                "schedule_type": "semi_synchronized",
                "coordination_windows": [
                    {"start": "10:00", "end": "14:00", "activity": "daily_operations"}
                ],
                "emergency_activation": "within_30_minutes",
                "content_synchronization": "hourly_batch",
                "cross_platform_coordination": False
            }
        else:
            return {
                "schedule_type": "loosely_coordinated",
                "coordination_windows": [
                    {"start": "20:00", "end": "23:00", "activity": "evening_activity"}
                ],
                "emergency_activation": "within_2_hours",
                "content_synchronization": "daily_batch",
                "cross_platform_coordination": False
            }
    
    def _calculate_network_metrics(self, bots: List[Dict], 
                                 connections: List[Dict]) -> Dict[str, Any]:
        """Calculate network-wide metrics"""
        
        total_followers = sum(bot["followers_count"] for bot in bots)
        total_posts = sum(bot["posts_count"] for bot in bots)
        avg_resistance = sum(bot["detection_resistance"]["overall_resistance"] for bot in bots) / len(bots)
        
        # Calculate bot type distribution
        type_counts = {}
        for bot in bots:
            bot_type = bot["bot_type"]
            type_counts[bot_type] = type_counts.get(bot_type, 0) + 1
        
        return {
            "total_network_reach": total_followers,
            "total_content_output": total_posts,
            "average_detection_resistance": avg_resistance,
            "network_density": len(connections) / (len(bots) * (len(bots) - 1) / 2),
            "bot_type_distribution": type_counts,
            "coordination_efficiency": random.uniform(0.6, 0.95),
            "operational_uptime": random.uniform(0.85, 0.99)
        }
    
    def _assess_network_detection_difficulty(self, bots: List[Dict], 
                                           coordination_level: str) -> str:
        """Assess how difficult the network is to detect"""
        
        avg_sophistication = sum(
            {"low": 1, "medium": 2, "high": 3}[bot["sophistication_level"]] 
            for bot in bots
        ) / len(bots)
        
        avg_resistance = sum(
            bot["detection_resistance"]["overall_resistance"] for bot in bots
        ) / len(bots)
        
        coordination_difficulty = {"low": 1, "medium": 2, "high": 3}[coordination_level]
        
        # Calculate overall difficulty score
        difficulty_score = (avg_sophistication + avg_resistance * 3 + coordination_difficulty) / 5
        
        if difficulty_score >= 2.5:
            return "VERY_HIGH"
        elif difficulty_score >= 2.0:
            return "HIGH"
        elif difficulty_score >= 1.5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_operational_objectives(self, coordination_level: str) -> List[str]:
        """Generate operational objectives for the bot network"""
        
        objectives = {
            "high": [
                "Large-scale disinformation campaign",
                "Government narrative manipulation",
                "Election interference operations",
                "Social unrest instigation",
                "International incident provocation"
            ],
            "medium": [
                "Targeted misinformation spread",
                "Specific policy opposition",
                "Local election influence",
                "Community division creation",
                "Corporate reputation damage"
            ],
            "low": [
                "General misinformation spread",
                "Social media engagement manipulation",
                "Basic narrative amplification",
                "Follower count inflation",
                "Simple content promotion"
            ]
        }
        
        return random.sample(objectives[coordination_level], 
                           random.randint(2, len(objectives[coordination_level])))
    
    def _assess_network_threat_level(self, bots: List[Dict], 
                                   coordination_level: str) -> str:
        """Assess the threat level of the bot network"""
        
        # Factors: network size, sophistication, coordination level, reach
        network_size = len(bots)
        total_reach = sum(bot["followers_count"] for bot in bots)
        avg_sophistication = sum(
            {"low": 1, "medium": 2, "high": 3}[bot["sophistication_level"]] 
            for bot in bots
        ) / len(bots)
        
        # Calculate threat score
        size_score = min(network_size / 100, 1.0)  # Normalize to max 1.0
        reach_score = min(total_reach / 100000, 1.0)  # Normalize to max 1.0
        sophistication_score = avg_sophistication / 3.0
        coordination_score = {"low": 0.3, "medium": 0.6, "high": 1.0}[coordination_level]
        
        threat_score = (size_score + reach_score + sophistication_score + coordination_score) / 4
        
        if threat_score >= 0.8:
            return "CRITICAL"
        elif threat_score >= 0.6:
            return "HIGH"
        elif threat_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
