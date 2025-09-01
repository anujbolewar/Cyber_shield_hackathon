"""
API Management Utilities for Police AI Monitor
Provides secure API key validation and testing functions
"""

import requests
import json
import time
from datetime import datetime
import random

class APITester:
    """Class for testing various API connections"""
    
    @staticmethod
    def test_openai_api(api_key):
        """Test OpenAI API connection"""
        if not api_key or api_key == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid API key provided',
                'status_code': 400
            }
        
        try:
            # Simulate API call (replace with actual OpenAI call in production)
            # headers = {
            #     'Authorization': f'Bearer {api_key}',
            #     'Content-Type': 'application/json'
            # }
            # response = requests.get('https://api.openai.com/v1/models', headers=headers, timeout=10)
            
            # For demo purposes, simulate success/failure
            time.sleep(random.uniform(0.5, 2.0))  # Simulate network delay
            success_rate = 0.8  # 80% success rate for demo
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'OpenAI API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(200, 800),
                    'model_access': ['gpt-3.5-turbo', 'text-davinci-003']
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid API key or quota exceeded',
                    'status_code': 401
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def test_twitter_api(bearer_token):
        """Test Twitter API v2 connection"""
        if not bearer_token or bearer_token == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid bearer token provided',
                'status_code': 400
            }
        
        try:
            # Simulate Twitter API call
            # headers = {'Authorization': f'Bearer {bearer_token}'}
            # response = requests.get('https://api.twitter.com/2/users/me', headers=headers, timeout=10)
            
            time.sleep(random.uniform(0.3, 1.5))
            success_rate = 0.75
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'Twitter API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(150, 600),
                    'rate_limit': '300 requests per 15 minutes'
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid bearer token or suspended account',
                    'status_code': 401
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def test_facebook_api(access_token):
        """Test Facebook Graph API connection"""
        if not access_token or access_token == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid access token provided',
                'status_code': 400
            }
        
        try:
            # Simulate Facebook API call
            # response = requests.get(f'https://graph.facebook.com/me?access_token={access_token}', timeout=10)
            
            time.sleep(random.uniform(0.4, 1.8))
            success_rate = 0.7
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'Facebook API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(200, 700),
                    'permissions': ['public_profile', 'pages_read_engagement']
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid access token or expired token',
                    'status_code': 401
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def test_telegram_api(bot_token):
        """Test Telegram Bot API connection"""
        if not bot_token or bot_token == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid bot token provided',
                'status_code': 400
            }
        
        try:
            # Simulate Telegram API call
            # response = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe', timeout=10)
            
            time.sleep(random.uniform(0.2, 1.0))
            success_rate = 0.85
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'Telegram Bot API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(100, 400),
                    'bot_info': {'username': 'police_monitor_bot', 'can_join_groups': True}
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid bot token',
                    'status_code': 401
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def test_news_api(api_key):
        """Test News API connection"""
        if not api_key or api_key == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid API key provided',
                'status_code': 400
            }
        
        try:
            # Simulate News API call
            # headers = {'X-API-Key': api_key}
            # response = requests.get('https://newsapi.org/v2/sources', headers=headers, timeout=10)
            
            time.sleep(random.uniform(0.5, 2.0))
            success_rate = 0.9
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'News API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(300, 900),
                    'sources_count': random.randint(50, 120)
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid API key or quota exceeded',
                    'status_code': 401
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def test_reddit_api(client_id, client_secret=None):
        """Test Reddit API connection"""
        if not client_id or client_id == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid client ID provided',
                'status_code': 400
            }
        
        try:
            # Simulate Reddit API call
            time.sleep(random.uniform(0.3, 1.2))
            success_rate = 0.75
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'Reddit API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(200, 600),
                    'rate_limit': '60 requests per minute'
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid credentials or rate limit exceeded',
                    'status_code': 401
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }
    
    @staticmethod
    def test_youtube_api(api_key):
        """Test YouTube Data API connection"""
        if not api_key or api_key == "●●●●●●●●":
            return {
                'success': False,
                'message': 'Invalid API key provided',
                'status_code': 400
            }
        
        try:
            # Simulate YouTube API call
            # response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key={api_key}', timeout=10)
            
            time.sleep(random.uniform(0.4, 1.6))
            success_rate = 0.8
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'message': 'YouTube Data API connection successful',
                    'status_code': 200,
                    'response_time': random.randint(250, 750),
                    'quota_usage': 'Search: 100 units per request'
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid API key or quota exceeded',
                    'status_code': 403
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'status_code': 500
            }

class APIKeyValidator:
    """Utility class for API key validation and formatting"""
    
    @staticmethod
    def validate_openai_key(api_key):
        """Validate OpenAI API key format"""
        if not api_key:
            return False, "API key cannot be empty"
        
        if not api_key.startswith('sk-'):
            return False, "OpenAI API keys should start with 'sk-'"
        
        if len(api_key) < 20:
            return False, "API key appears to be too short"
        
        return True, "Valid format"
    
    @staticmethod
    def validate_twitter_token(bearer_token):
        """Validate Twitter bearer token format"""
        if not bearer_token:
            return False, "Bearer token cannot be empty"
        
        if len(bearer_token) < 50:
            return False, "Bearer token appears to be too short"
        
        return True, "Valid format"
    
    @staticmethod
    def validate_facebook_token(access_token):
        """Validate Facebook access token format"""
        if not access_token:
            return False, "Access token cannot be empty"
        
        if len(access_token) < 50:
            return False, "Access token appears to be too short"
        
        return True, "Valid format"
    
    @staticmethod
    def validate_telegram_token(bot_token):
        """Validate Telegram bot token format"""
        if not bot_token:
            return False, "Bot token cannot be empty"
        
        if ':' not in bot_token:
            return False, "Telegram bot tokens should contain ':' character"
        
        parts = bot_token.split(':')
        if len(parts) != 2:
            return False, "Invalid bot token format"
        
        try:
            int(parts[0])  # Bot ID should be numeric
        except ValueError:
            return False, "First part of token should be numeric (bot ID)"
        
        return True, "Valid format"
    
    @staticmethod
    def mask_api_key(api_key, visible_chars=4):
        """Mask API key for display purposes"""
        if not api_key:
            return ""
        
        if len(api_key) <= visible_chars * 2:
            return "●" * len(api_key)
        
        return api_key[:visible_chars] + "●" * (len(api_key) - visible_chars * 2) + api_key[-visible_chars:]

def get_api_setup_links():
    """Return dictionary of API setup links and information"""
    return {
        'openai': {
            'name': 'OpenAI',
            'url': 'https://platform.openai.com/api-keys',
            'description': 'AI-powered text analysis and sentiment detection',
            'instructions': [
                'Create an OpenAI account',
                'Navigate to API Keys section',
                'Click "Create new secret key"',
                'Copy the key (starts with sk-)',
                'Set usage limits for security'
            ],
            'pricing': 'Pay-per-use model, starts at $0.002/1K tokens'
        },
        'twitter': {
            'name': 'Twitter/X',
            'url': 'https://developer.twitter.com/en/portal/dashboard',
            'description': 'Social media monitoring and real-time feeds',
            'instructions': [
                'Apply for Twitter Developer account',
                'Create a new project/app',
                'Generate Bearer Token',
                'Copy the Bearer Token',
                'Configure API permissions'
            ],
            'pricing': 'Free tier: 10,000 tweets/month, Paid: $100+/month'
        },
        'facebook': {
            'name': 'Facebook/Meta',
            'url': 'https://developers.facebook.com/apps/',
            'description': 'Facebook and Instagram content monitoring',
            'instructions': [
                'Create Facebook Developer account',
                'Create new app',
                'Add Facebook Graph API',
                'Generate access token',
                'Configure app permissions'
            ],
            'pricing': 'Free with rate limits, Business API available'
        },
        'telegram': {
            'name': 'Telegram',
            'url': 'https://core.telegram.org/bots#6-botfather',
            'description': 'Telegram channel and group monitoring',
            'instructions': [
                'Message @BotFather on Telegram',
                'Send /newbot command',
                'Choose bot name and username',
                'Copy the HTTP API token',
                'Configure bot permissions'
            ],
            'pricing': 'Free'
        },
        'news_api': {
            'name': 'News API',
            'url': 'https://newsapi.org/register',
            'description': 'Global news aggregation and monitoring',
            'instructions': [
                'Register for News API account',
                'Verify email address',
                'Copy your API key',
                'Choose subscription plan',
                'Test with sample requests'
            ],
            'pricing': 'Free: 100 requests/day, Paid: $449+/month'
        },
        'reddit': {
            'name': 'Reddit',
            'url': 'https://www.reddit.com/prefs/apps',
            'description': 'Reddit community monitoring and analysis',
            'instructions': [
                'Create Reddit account',
                'Go to App preferences',
                'Create new app (script type)',
                'Copy client ID and secret',
                'Use credentials for API access'
            ],
            'pricing': 'Free with rate limits'
        },
        'youtube': {
            'name': 'YouTube',
            'url': 'https://console.cloud.google.com/apis/library/youtube.googleapis.com',
            'description': 'YouTube video and comment monitoring',
            'instructions': [
                'Create Google Cloud project',
                'Enable YouTube Data API v3',
                'Create API credentials',
                'Copy the API key',
                'Set quota limits'
            ],
            'pricing': 'Free tier: 10,000 units/day, Paid: usage-based'
        }
    }
