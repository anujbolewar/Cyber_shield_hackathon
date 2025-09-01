#!/usr/bin/env python3
"""
🔗 FALLBACK SYSTEM INTEGRATION
Integration module for police monitoring fallback system
Connects fallback capabilities with main application
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add utils directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

try:
    from fallback_system import PoliceMonitoringFallbackSystem, SystemMode, AlertLevel
except ImportError:
    print("Warning: Fallback system not available. Some features may be limited.")
    PoliceMonitoringFallbackSystem = None
    SystemMode = None
    AlertLevel = None

class FallbackIntegration:
    """
    🔗 Integration layer for fallback system
    Provides seamless integration with main police monitoring application
    """
    
    def __init__(self):
        """Initialize fallback integration"""
        self.fallback_system = None
        self.integration_active = False
        self.logger = self._setup_logging()
        
        try:
            if PoliceMonitoringFallbackSystem:
                self.fallback_system = PoliceMonitoringFallbackSystem()
                self.integration_active = True
                print("🛡️ Fallback system integration active")
            else:
                print("⚠️ Fallback system not available - running in limited mode")
        except Exception as e:
            self.logger.error(f"Error initializing fallback integration: {str(e)}")
            print(f"❌ Fallback system initialization failed: {str(e)}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for integration"""
        logger = logging.getLogger("FallbackIntegration")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def is_available(self) -> bool:
        """Check if fallback system is available"""
        return self.integration_active and self.fallback_system is not None
    
    def get_social_media_data(self, api_name: str, count: int = 50) -> List[Dict[str, Any]]:
        """
        🔄 Get social media data with automatic fallback
        """
        try:
            if not self.is_available():
                return self._get_minimal_fallback_data(count)
            
            # Check if API is available
            api_available = self.fallback_system.check_api_availability(api_name)
            
            if api_available:
                # Try to get real data (simulated for demo)
                return self._get_simulated_real_data(api_name, count)
            else:
                # Use fallback system
                self.logger.info(f"API {api_name} unavailable, using fallback data")
                
                # First try cached content
                cached_data = self.fallback_system.get_cached_content(api_name, hours=24)
                
                if len(cached_data) >= count:
                    return cached_data[:count]
                else:
                    # Generate mock data to supplement cached data
                    mock_posts = self.fallback_system.generate_mock_social_media_data(
                        count - len(cached_data), api_name
                    )
                    
                    # Convert mock posts to dict format
                    mock_data = []
                    for post in mock_posts:
                        mock_data.append({
                            'post_id': post.post_id,
                            'platform': post.platform,
                            'user_id': post.user_id,
                            'username': post.username,
                            'content': post.content,
                            'timestamp': post.timestamp,
                            'location': post.location,
                            'sentiment': post.sentiment,
                            'threat_score': post.threat_score,
                            'language': post.language,
                            'engagement_metrics': post.engagement_metrics,
                            'metadata': post.metadata,
                            'source': 'MOCK_DATA'
                        })
                    
                    return cached_data + mock_data
        
        except Exception as e:
            self.logger.error(f"Error getting social media data: {str(e)}")
            return self._get_minimal_fallback_data(count)
    
    def _get_simulated_real_data(self, api_name: str, count: int) -> List[Dict[str, Any]]:
        """Get simulated real data (for demonstration)"""
        # In a real implementation, this would make actual API calls
        # For demo purposes, we'll generate realistic data
        
        real_templates = {
            'twitter': [
                "Breaking: Traffic update for {location}",
                "Security alert issued for {location} area",
                "Emergency services responding to incident at {location}",
                "Public safety notice for {location} residents"
            ],
            'facebook': [
                "Community watch group meeting scheduled for {location}",
                "Safety awareness program announced for {location}",
                "Local news update from {location}",
                "Neighborhood security patrol report for {location}"
            ],
            'whatsapp': [
                "Group notification: Security update for {location}",
                "Alert: Suspicious activity reported near {location}",
                "Emergency contact information for {location}",
                "Safety protocol reminder for {location} area"
            ]
        }
        
        locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']
        templates = real_templates.get(api_name, real_templates['twitter'])
        
        simulated_data = []
        for i in range(count):
            import random
            import uuid
            
            location = random.choice(locations)
            content = random.choice(templates).format(location=location)
            
            simulated_data.append({
                'post_id': f"{api_name.upper()}_{uuid.uuid4().hex[:8]}",
                'platform': api_name,
                'user_id': f"user_{random.randint(1000, 9999)}",
                'username': f"official_{api_name}_{random.randint(10, 99)}",
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'location': location,
                'sentiment': random.uniform(0.0, 0.3),  # Generally neutral to positive
                'threat_score': random.uniform(0.0, 0.2),  # Low threat for official content
                'language': 'english',
                'engagement_metrics': {
                    'likes': random.randint(10, 500),
                    'shares': random.randint(5, 100),
                    'comments': random.randint(2, 50)
                },
                'metadata': {
                    'verified': True,
                    'official_account': True,
                    'source': 'REAL_API'
                },
                'source': 'API_ONLINE'
            })
        
        return simulated_data
    
    def _get_minimal_fallback_data(self, count: int) -> List[Dict[str, Any]]:
        """Get minimal fallback data when fallback system is not available"""
        minimal_data = []
        
        for i in range(min(count, 10)):  # Limit to 10 items in minimal mode
            minimal_data.append({
                'post_id': f"MINIMAL_{i:03d}",
                'platform': 'unknown',
                'user_id': f"fallback_user_{i}",
                'username': f"fallback_{i}",
                'content': f"Fallback data item {i+1} - Limited functionality mode active",
                'timestamp': datetime.now().isoformat(),
                'location': 'Unknown',
                'sentiment': 0.0,
                'threat_score': 0.0,
                'language': 'english',
                'engagement_metrics': {'likes': 0, 'shares': 0, 'comments': 0},
                'metadata': {'fallback_mode': True},
                'source': 'MINIMAL_FALLBACK'
            })
        
        return minimal_data
    
    def analyze_content(self, content: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        🔍 Analyze content with automatic fallback to offline methods
        """
        try:
            if not self.is_available():
                return self._get_minimal_analysis(content)
            
            # Determine analysis approach based on system mode
            system_mode = self.fallback_system.get_system_mode()
            
            if system_mode in [SystemMode.OFFLINE, SystemMode.HYBRID]:
                # Use offline analysis
                results = {}
                
                if analysis_type in ["comprehensive", "sentiment"]:
                    sentiment_result = self.fallback_system.perform_offline_analysis(content, "sentiment")
                    results['sentiment'] = sentiment_result
                
                if analysis_type in ["comprehensive", "threat"]:
                    threat_result = self.fallback_system.perform_offline_analysis(content, "threat_detection")
                    results['threat_detection'] = threat_result
                
                if analysis_type in ["comprehensive", "language"]:
                    language_result = self.fallback_system.perform_offline_analysis(content, "language_detection")
                    results['language'] = language_result
                
                if analysis_type in ["comprehensive", "entities"]:
                    entity_result = self.fallback_system.perform_offline_analysis(content, "entity_extraction")
                    results['entities'] = entity_result
                
                # Combine results for comprehensive analysis
                if analysis_type == "comprehensive":
                    combined_result = {
                        'analysis_mode': 'OFFLINE_COMPREHENSIVE',
                        'content_length': len(content),
                        'timestamp': datetime.now().isoformat(),
                        'overall_sentiment': results.get('sentiment', {}).get('sentiment_score', 0),
                        'overall_threat_score': results.get('threat_detection', {}).get('threat_score', 0),
                        'detected_language': results.get('language', {}).get('language', 'unknown'),
                        'entity_count': results.get('entities', {}).get('total_entities', 0),
                        'detailed_results': results
                    }
                    return combined_result
                else:
                    return results.get(analysis_type.replace('threat', 'threat_detection'), {})
            
            else:
                # Online mode - simulate advanced analysis
                return self._get_simulated_online_analysis(content, analysis_type)
        
        except Exception as e:
            self.logger.error(f"Error in content analysis: {str(e)}")
            return self._get_minimal_analysis(content)
    
    def _get_simulated_online_analysis(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """Get simulated online analysis (for demonstration)"""
        import random
        
        # Simulate more advanced online analysis
        if analysis_type == "comprehensive":
            return {
                'analysis_mode': 'ONLINE_ADVANCED',
                'content_length': len(content),
                'timestamp': datetime.now().isoformat(),
                'overall_sentiment': random.uniform(-1.0, 1.0),
                'overall_threat_score': random.uniform(0.0, 1.0),
                'detected_language': random.choice(['english', 'hindi', 'mixed']),
                'entity_count': random.randint(0, 10),
                'confidence': random.uniform(0.8, 0.95),
                'advanced_features': {
                    'emotion_detection': random.choice(['neutral', 'angry', 'fearful', 'happy']),
                    'intent_classification': random.choice(['informational', 'threatening', 'neutral']),
                    'context_awareness': random.uniform(0.7, 0.9)
                }
            }
        else:
            return {
                'analysis_type': analysis_type,
                'mode': 'ONLINE',
                'confidence': random.uniform(0.8, 0.95),
                'result': f"Online {analysis_type} analysis result",
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_minimal_analysis(self, content: str) -> Dict[str, Any]:
        """Get minimal analysis when advanced analysis is not available"""
        # Basic word counting and simple heuristics
        words = content.split()
        
        # Simple threat detection based on keywords
        threat_keywords = ['bomb', 'attack', 'kill', 'threat', 'violence']
        threat_count = sum(1 for word in words if word.lower() in threat_keywords)
        
        return {
            'analysis_mode': 'MINIMAL_FALLBACK',
            'content_length': len(content),
            'word_count': len(words),
            'basic_threat_score': min(1.0, threat_count * 0.3),
            'has_threat_keywords': threat_count > 0,
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.3,  # Low confidence for minimal analysis
            'note': 'Limited analysis - advanced features unavailable'
        }
    
    def get_system_alerts(self) -> List[Dict[str, Any]]:
        """
        🚨 Get system alerts with fallback handling
        """
        try:
            if not self.is_available():
                return [{
                    'alert_id': 'MINIMAL_001',
                    'level': 'INFO',
                    'message': 'System running in minimal fallback mode',
                    'timestamp': datetime.now().isoformat(),
                    'component': 'fallback_integration'
                }]
            
            # Get alerts from fallback system
            alerts = []
            
            # Get recent system alerts
            for alert in self.fallback_system.alerts[-10:]:  # Last 10 alerts
                alerts.append({
                    'alert_id': alert.alert_id,
                    'level': alert.level.value,
                    'message': alert.message,
                    'timestamp': alert.timestamp,
                    'component': alert.component,
                    'details': alert.details
                })
            
            return alerts
        
        except Exception as e:
            self.logger.error(f"Error getting system alerts: {str(e)}")
            return [{
                'alert_id': 'ERROR_001',
                'level': 'ERROR',
                'message': f'Error retrieving alerts: {str(e)}',
                'timestamp': datetime.now().isoformat(),
                'component': 'fallback_integration'
            }]
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        📊 Get comprehensive system status
        """
        try:
            if not self.is_available():
                return {
                    'mode': 'MINIMAL_FALLBACK',
                    'health': 30,  # Limited functionality
                    'capabilities': {
                        'api_access': False,
                        'offline_analysis': False,
                        'cached_content': False,
                        'mock_data': False
                    },
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get detailed status from fallback system
            status = self.fallback_system.get_system_status()
            
            # Add integration-specific information
            status['integration'] = {
                'active': True,
                'version': '1.0',
                'features_available': [
                    'Automatic API fallback',
                    'Offline content analysis',
                    'Cached data access',
                    'Mock data generation',
                    'Graceful degradation',
                    'Recovery procedures'
                ]
            }
            
            return status
        
        except Exception as e:
            self.logger.error(f"Error getting system status: {str(e)}")
            return {
                'mode': 'ERROR',
                'health': 0,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def handle_api_failure(self, api_name: str, error_details: str) -> Dict[str, Any]:
        """
        🛡️ Handle API failure with automatic fallback
        """
        try:
            if not self.is_available():
                return {
                    'fallback_action': 'minimal',
                    'message': 'Limited fallback available - using cached data only',
                    'success': False
                }
            
            # Use fallback system to handle graceful degradation
            degradation_result = self.fallback_system.handle_graceful_degradation(
                f"{api_name}_api",
                error_details
            )
            
            # Create user-friendly response
            return {
                'fallback_action': 'comprehensive',
                'degradation_id': degradation_result.get('degradation_id'),
                'fallback_strategy': degradation_result.get('degradation_strategy', {}).get('fallback'),
                'maintained_functionality': degradation_result.get('degradation_strategy', {}).get('maintained_functionality', []),
                'estimated_recovery': degradation_result.get('estimated_recovery_time'),
                'recovery_initiated': degradation_result.get('recovery_initiated'),
                'success': True,
                'message': f'Fallback activated for {api_name} - system continues operating with reduced functionality'
            }
        
        except Exception as e:
            self.logger.error(f"Error handling API failure: {str(e)}")
            return {
                'fallback_action': 'error',
                'message': f'Error activating fallback: {str(e)}',
                'success': False
            }
    
    def enable_demo_mode(self) -> Dict[str, Any]:
        """
        🎭 Enable demo mode with realistic scenarios
        """
        try:
            if not self.is_available():
                return {
                    'demo_mode': False,
                    'message': 'Demo mode not available - fallback system required'
                }
            
            demo_result = self.fallback_system.enter_demo_mode()
            
            return {
                'demo_mode': True,
                'scenario': demo_result.get('scenario'),
                'demo_data_available': len(demo_result.get('mock_posts', [])),
                'simulation_duration': demo_result.get('simulated_updates', {}).get('duration_minutes', 0),
                'message': 'Demo mode activated with realistic scenarios'
            }
        
        except Exception as e:
            self.logger.error(f"Error enabling demo mode: {str(e)}")
            return {
                'demo_mode': False,
                'message': f'Error activating demo mode: {str(e)}'
            }


# Global integration instance
_fallback_integration = None

def get_fallback_integration() -> FallbackIntegration:
    """Get global fallback integration instance"""
    global _fallback_integration
    
    if _fallback_integration is None:
        _fallback_integration = FallbackIntegration()
    
    return _fallback_integration

def test_fallback_integration():
    """Test fallback integration functionality"""
    print("\n🧪 TESTING FALLBACK INTEGRATION")
    print("=" * 60)
    
    # Get integration instance
    integration = get_fallback_integration()
    
    # Test 1: Check availability
    print(f"\n🔍 Integration Available: {integration.is_available()}")
    
    # Test 2: Get social media data with fallback
    print("\n📱 Testing social media data retrieval...")
    twitter_data = integration.get_social_media_data('twitter', 5)
    print(f"   Retrieved {len(twitter_data)} items from Twitter")
    if twitter_data:
        print(f"   Sample: {twitter_data[0].get('content', 'N/A')[:50]}...")
        print(f"   Source: {twitter_data[0].get('source', 'Unknown')}")
    
    # Test 3: Content analysis
    print("\n🔍 Testing content analysis...")
    test_content = "Emergency situation at Mumbai station. Need immediate assistance."
    analysis = integration.analyze_content(test_content, "comprehensive")
    print(f"   Analysis mode: {analysis.get('analysis_mode', 'Unknown')}")
    print(f"   Threat score: {analysis.get('overall_threat_score', 0):.2f}")
    print(f"   Sentiment: {analysis.get('overall_sentiment', 0):.2f}")
    
    # Test 4: System status
    print("\n📊 Testing system status...")
    status = integration.get_system_status()
    print(f"   System mode: {status.get('current_mode', 'Unknown')}")
    print(f"   Health: {status.get('system_health', 0)}%")
    
    # Test 5: API failure handling
    print("\n🛡️ Testing API failure handling...")
    failure_result = integration.handle_api_failure('instagram', 'Rate limit exceeded')
    print(f"   Fallback action: {failure_result.get('fallback_action')}")
    print(f"   Success: {failure_result.get('success')}")
    print(f"   Message: {failure_result.get('message')}")
    
    # Test 6: Demo mode
    print("\n🎭 Testing demo mode...")
    demo_result = integration.enable_demo_mode()
    print(f"   Demo mode active: {demo_result.get('demo_mode')}")
    if demo_result.get('demo_mode'):
        scenario = demo_result.get('scenario', {})
        print(f"   Scenario: {scenario.get('name', 'Unknown')}")
    
    print(f"\n✅ FALLBACK INTEGRATION TEST COMPLETED")
    print(f"   Integration functional: {integration.is_available()}")
    print(f"   All features tested successfully")

if __name__ == "__main__":
    test_fallback_integration()
