#!/usr/bin/env python3
"""
🐦 TWITTER MONITORING CONFIGURATION
Centralized configuration for Twitter API integration and monitoring settings
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TwitterAPIConfig:
    """Twitter API configuration settings"""
    bearer_token: str = ""
    api_key: str = ""
    api_secret: str = ""
    access_token: str = ""
    access_token_secret: str = ""
    webhook_url: str = ""
    rate_limit_per_minute: int = 300
    stream_timeout: int = 120

@dataclass 
class MonitoringConfig:
    """Monitoring behavior configuration"""
    # Keywords for filtering
    india_keywords: List[str] = None
    threat_keywords: Dict[str, List[str]] = None
    
    # Analysis thresholds
    bot_probability_threshold: float = 0.7
    threat_escalation_threshold: float = 0.8
    engagement_velocity_threshold: float = 50.0
    
    # Geographic settings
    geo_cluster_radius_km: float = 10.0
    india_bbox: List[float] = None  # [min_lat, min_lng, max_lat, max_lng]
    
    # Alert settings
    enable_email_alerts: bool = True
    enable_sms_alerts: bool = False
    alert_cooldown_minutes: int = 15
    
    # Database settings
    max_tweets_stored: int = 100000
    data_retention_days: int = 90
    
    # Evidence capture
    capture_screenshots: bool = True
    evidence_storage_path: str = "evidence/twitter"
    
    def __post_init__(self):
        """Initialize default values"""
        if self.india_keywords is None:
            self.india_keywords = [
                # Major cities
                "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad",
                "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur",
                "Indore", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ludhiana",
                "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan",
                "Vasai", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar",
                
                # States and regions
                "Maharashtra", "Karnataka", "Tamil Nadu", "West Bengal", "Gujarat",
                "Rajasthan", "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh",
                "Bihar", "Odisha", "Telangana", "Andhra Pradesh", "Kerala",
                "Assam", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh",
                
                # General India terms
                "India", "Bharat", "Indian", "Hindustan", "Desi", "Modi",
                "BJP", "Congress", "Parliament", "Lok Sabha", "Rajya Sabha",
                
                # Law enforcement terms
                "police", "constable", "inspector", "commissioner", "IPS",
                "security", "crime", "theft", "robbery", "murder", "rape",
                "terrorism", "bomb", "blast", "attack", "threat", "violence",
                "protest", "rally", "bandh", "hartal", "strike", "demonstration",
                
                # Emergency and safety
                "emergency", "ambulance", "fire", "accident", "disaster",
                "flood", "earthquake", "cyclone", "storm", "rescue",
                "missing", "kidnap", "abduction", "suspicious", "drugs",
                "trafficking", "smuggling", "corruption", "bribe", "scam"
            ]
        
        if self.threat_keywords is None:
            self.threat_keywords = {
                "CRITICAL": [
                    "bomb", "blast", "explosion", "terrorist", "terrorism",
                    "attack", "killing", "murder", "massacre", "shoot",
                    "gun", "weapon", "threat", "kidnap", "hostage"
                ],
                "HIGH": [
                    "violence", "riot", "fight", "clash", "assault",
                    "robbery", "theft", "burglary", "rape", "molest",
                    "drug", "smuggling", "trafficking", "illegal", "crime"
                ],
                "MEDIUM": [
                    "protest", "demonstration", "rally", "bandh", "strike",
                    "accident", "injury", "fire", "emergency", "missing",
                    "suspicious", "concern", "worry", "problem", "issue"
                ],
                "LOW": [
                    "traffic", "jam", "delay", "closure", "diversion",
                    "maintenance", "construction", "festival", "celebration",
                    "gathering", "meeting", "event", "announcement"
                ]
            }
        
        if self.india_bbox is None:
            # Bounding box for India (approximate)
            self.india_bbox = [6.0, 68.0, 37.0, 98.0]  # [min_lat, min_lng, max_lat, max_lng]

class TwitterConfig:
    """
    🔧 Twitter monitoring configuration manager
    Handles loading, saving, and validating configuration settings
    """
    
    def __init__(self, config_file: str = "config/twitter_config.json"):
        """Initialize configuration manager"""
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.api_config = TwitterAPIConfig()
        self.monitoring_config = MonitoringConfig()
        
        # Load existing configuration
        self.load_config()
    
    def load_config(self) -> bool:
        """
        📖 Load configuration from file
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Load API config
                api_data = config_data.get('api', {})
                for key, value in api_data.items():
                    if hasattr(self.api_config, key):
                        setattr(self.api_config, key, value)
                
                # Load monitoring config
                monitoring_data = config_data.get('monitoring', {})
                for key, value in monitoring_data.items():
                    if hasattr(self.monitoring_config, key):
                        setattr(self.monitoring_config, key, value)
                
                print(f"✅ Configuration loaded from {self.config_file}")
                return True
            else:
                print(f"ℹ️ No existing config found, using defaults")
                self.save_config()  # Save default config
                return False
                
        except Exception as e:
            print(f"❌ Error loading config: {str(e)}")
            return False
    
    def save_config(self) -> bool:
        """
        💾 Save configuration to file
        """
        try:
            config_data = {
                'api': {
                    'bearer_token': self.api_config.bearer_token,
                    'api_key': self.api_config.api_key,
                    'api_secret': self.api_config.api_secret,
                    'access_token': self.api_config.access_token,
                    'access_token_secret': self.api_config.access_token_secret,
                    'webhook_url': self.api_config.webhook_url,
                    'rate_limit_per_minute': self.api_config.rate_limit_per_minute,
                    'stream_timeout': self.api_config.stream_timeout
                },
                'monitoring': {
                    'india_keywords': self.monitoring_config.india_keywords,
                    'threat_keywords': self.monitoring_config.threat_keywords,
                    'bot_probability_threshold': self.monitoring_config.bot_probability_threshold,
                    'threat_escalation_threshold': self.monitoring_config.threat_escalation_threshold,
                    'engagement_velocity_threshold': self.monitoring_config.engagement_velocity_threshold,
                    'geo_cluster_radius_km': self.monitoring_config.geo_cluster_radius_km,
                    'india_bbox': self.monitoring_config.india_bbox,
                    'enable_email_alerts': self.monitoring_config.enable_email_alerts,
                    'enable_sms_alerts': self.monitoring_config.enable_sms_alerts,
                    'alert_cooldown_minutes': self.monitoring_config.alert_cooldown_minutes,
                    'max_tweets_stored': self.monitoring_config.max_tweets_stored,
                    'data_retention_days': self.monitoring_config.data_retention_days,
                    'capture_screenshots': self.monitoring_config.capture_screenshots,
                    'evidence_storage_path': self.monitoring_config.evidence_storage_path
                },
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'version': '1.0.0'
                }
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving config: {str(e)}")
            return False
    
    def validate_api_config(self) -> Dict[str, bool]:
        """
        ✅ Validate API configuration
        """
        validation_results = {
            'bearer_token': bool(self.api_config.bearer_token and len(self.api_config.bearer_token) > 10),
            'api_credentials': bool(self.api_config.api_key and self.api_config.api_secret),
            'access_tokens': bool(self.api_config.access_token and self.api_config.access_token_secret),
            'rate_limits': self.api_config.rate_limit_per_minute > 0,
            'timeout_settings': self.api_config.stream_timeout > 0
        }
        
        return validation_results
    
    def get_stream_rules(self) -> List[Dict[str, str]]:
        """
        📝 Generate Twitter stream rules from keywords
        """
        rules = []
        
        # India general keywords (first 25 keywords to avoid rule length limits)
        india_rule = " OR ".join(self.monitoring_config.india_keywords[:25])
        rules.append({
            "value": india_rule,
            "tag": "india_general"
        })
        
        # Threat level rules
        for level, keywords in self.monitoring_config.threat_keywords.items():
            if keywords:
                threat_rule = " OR ".join(keywords[:10])  # Limit to 10 keywords per rule
                rules.append({
                    "value": threat_rule,
                    "tag": f"threat_{level.lower()}"
                })
        
        # Geographic rule for India
        bbox = self.monitoring_config.india_bbox
        if bbox and len(bbox) == 4:
            geo_rule = f"bounding_box:[{bbox[1]} {bbox[0]} {bbox[3]} {bbox[2]}]"
            rules.append({
                "value": geo_rule,
                "tag": "india_geographic"
            })
        
        return rules
    
    def update_keywords(self, keyword_type: str, keywords: List[str]) -> bool:
        """
        🔄 Update specific keyword lists
        """
        try:
            if keyword_type == "india":
                self.monitoring_config.india_keywords = keywords
            elif keyword_type in self.monitoring_config.threat_keywords:
                self.monitoring_config.threat_keywords[keyword_type] = keywords
            else:
                print(f"❌ Unknown keyword type: {keyword_type}")
                return False
            
            return self.save_config()
            
        except Exception as e:
            print(f"❌ Error updating keywords: {str(e)}")
            return False
    
    def get_alert_settings(self) -> Dict[str, Any]:
        """
        📢 Get alert configuration settings
        """
        return {
            'email_enabled': self.monitoring_config.enable_email_alerts,
            'sms_enabled': self.monitoring_config.enable_sms_alerts,
            'cooldown_minutes': self.monitoring_config.alert_cooldown_minutes,
            'bot_threshold': self.monitoring_config.bot_probability_threshold,
            'threat_threshold': self.monitoring_config.threat_escalation_threshold,
            'engagement_threshold': self.monitoring_config.engagement_velocity_threshold
        }
    
    def export_config(self, export_path: str) -> bool:
        """
        📤 Export configuration to specified path
        """
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy current config to export location
            with open(self.config_file, 'r') as source:
                config_data = json.load(source)
            
            # Add export metadata
            config_data['export_metadata'] = {
                'exported_at': datetime.now().isoformat(),
                'original_file': str(self.config_file),
                'export_version': '1.0.0'
            }
            
            with open(export_file, 'w') as target:
                json.dump(config_data, target, indent=2)
            
            print(f"✅ Configuration exported to {export_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting config: {str(e)}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """
        📥 Import configuration from specified path
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                print(f"❌ Import file not found: {import_file}")
                return False
            
            # Backup current config
            backup_path = self.config_file.with_suffix('.backup.json')
            if self.config_file.exists():
                with open(self.config_file, 'r') as source:
                    with open(backup_path, 'w') as backup:
                        backup.write(source.read())
            
            # Import new config
            with open(import_file, 'r') as source:
                with open(self.config_file, 'w') as target:
                    target.write(source.read())
            
            # Reload configuration
            self.load_config()
            
            print(f"✅ Configuration imported from {import_file}")
            print(f"📁 Backup saved to {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing config: {str(e)}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """
        🔄 Reset configuration to default values
        """
        try:
            # Backup current config
            backup_path = self.config_file.with_suffix('.backup.json')
            if self.config_file.exists():
                with open(self.config_file, 'r') as source:
                    with open(backup_path, 'w') as backup:
                        backup.write(source.read())
            
            # Reset to defaults
            self.api_config = TwitterAPIConfig()
            self.monitoring_config = MonitoringConfig()
            
            # Save default config
            self.save_config()
            
            print(f"✅ Configuration reset to defaults")
            print(f"📁 Backup saved to {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error resetting config: {str(e)}")
            return False


def test_twitter_config():
    """Test Twitter configuration functionality"""
    print("\n🧪 TESTING TWITTER CONFIGURATION")
    print("=" * 80)
    
    # Test 1: Initialize configuration
    print("\n1️⃣ Testing Configuration Initialization...")
    config = TwitterConfig("test_config.json")
    init_success = config.config_file.exists()
    print(f"   Status: {'✅ INITIALIZED' if init_success else '❌ FAILED'}")
    
    # Test 2: Validate default settings
    print("\n2️⃣ Testing Default Settings Validation...")
    validation = config.validate_api_config()
    default_valid = len(config.monitoring_config.india_keywords) > 0
    print(f"   Status: {'✅ VALID' if default_valid else '❌ INVALID'}")
    print(f"      🇮🇳 India Keywords: {len(config.monitoring_config.india_keywords)}")
    print(f"      🚨 Threat Keywords: {sum(len(v) for v in config.monitoring_config.threat_keywords.values())}")
    
    # Test 3: Stream rules generation
    print("\n3️⃣ Testing Stream Rules Generation...")
    rules = config.get_stream_rules()
    rules_valid = len(rules) > 0 and all('value' in rule and 'tag' in rule for rule in rules)
    print(f"   Status: {'✅ GENERATED' if rules_valid else '❌ FAILED'}")
    print(f"      📝 Rules Generated: {len(rules)}")
    
    # Test 4: Configuration save/load
    print("\n4️⃣ Testing Configuration Persistence...")
    save_success = config.save_config()
    
    # Modify and reload
    original_keywords = config.monitoring_config.india_keywords.copy()
    config.monitoring_config.india_keywords.append("TestCity")
    config.save_config()
    
    # Create new instance and load
    config2 = TwitterConfig("test_config.json")
    load_success = "TestCity" in config2.monitoring_config.india_keywords
    print(f"   Status: {'✅ PERSISTENT' if load_success else '❌ FAILED'}")
    
    # Test 5: Alert settings
    print("\n5️⃣ Testing Alert Settings...")
    alert_settings = config.get_alert_settings()
    alerts_valid = all(key in alert_settings for key in ['email_enabled', 'bot_threshold', 'engagement_threshold'])
    print(f"   Status: {'✅ CONFIGURED' if alerts_valid else '❌ MISSING'}")
    
    # Cleanup
    try:
        Path("test_config.json").unlink()
        print("   🧹 Test files cleaned up")
    except:
        pass
    
    # Summary
    print(f"\n📊 TWITTER CONFIGURATION TEST SUMMARY")
    print("=" * 80)
    
    results = [
        ('Configuration Initialization', init_success),
        ('Default Settings Validation', default_valid),
        ('Stream Rules Generation', rules_valid),
        ('Configuration Persistence', load_success),
        ('Alert Settings', alerts_valid)
    ]
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall Success Rate: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🏆 TWITTER CONFIGURATION SYSTEM FULLY OPERATIONAL!")
    elif passed_tests >= total_tests * 0.8:
        print("🥇 TWITTER CONFIGURATION SYSTEM WORKING WELL!")
    else:
        print("⚠️ TWITTER CONFIGURATION SYSTEM NEEDS ATTENTION")
    
    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': passed_tests / total_tests,
        'results': dict(results)
    }


if __name__ == "__main__":
    test_twitter_config()
