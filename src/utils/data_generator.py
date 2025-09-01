"""
Data generation utilities for social media monitoring demo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(platforms, keywords, time_range):
    """Generate sample social media data for demonstration"""
    
    # Determine number of records based on time range
    if time_range == "Last Hour":
        num_records = 100
        start_date = datetime.now() - timedelta(hours=1)
    elif time_range == "Last 6 Hours":
        num_records = 500
        start_date = datetime.now() - timedelta(hours=6)
    elif time_range == "Last 24 Hours":
        num_records = 1000
        start_date = datetime.now() - timedelta(days=1)
    elif time_range == "Last 7 Days":
        num_records = 5000
        start_date = datetime.now() - timedelta(days=7)
    else:  # Last 30 Days
        num_records = 10000
        start_date = datetime.now() - timedelta(days=30)
    
    # Generate timestamps
    timestamps = [
        start_date + timedelta(
            seconds=random.randint(0, int((datetime.now() - start_date).total_seconds()))
        ) for _ in range(num_records)
    ]
    timestamps.sort()
    
    # Sample content templates
    content_templates = [
        "Just tried {brand} and I'm absolutely loving it! #amazing #customerservice",
        "Having issues with {brand} today. Hope they fix this soon. #frustrated",
        "Great experience with {brand}! Highly recommend to everyone. #satisfied",
        "The new {brand} update is fantastic! Love the new features. #innovation",
        "Could be better. {brand} needs to improve their service. #feedback",
        "Wow! {brand} exceeded my expectations. Five stars! #excellence",
        "Not impressed with {brand} lately. What happened? #disappointed",
        "Thank you {brand} for the quick response! Great support team. #grateful",
        "Been using {brand} for years. Still the best! #loyal",
        "First time trying {brand}. So far so good! #newcustomer"
    ]
    
    # Generate sample data
    data = []
    for i in range(num_records):
        platform = random.choice(platforms) if platforms else random.choice(['Twitter', 'Facebook', 'Instagram'])
        sentiment_score = np.random.normal(0.2, 0.4)  # Slightly positive bias
        sentiment_score = max(-1, min(1, sentiment_score))  # Clamp between -1 and 1
        
        # Categorize sentiment
        if sentiment_score > 0.2:
            sentiment_category = 'Positive'
        elif sentiment_score < -0.2:
            sentiment_category = 'Negative'
        else:
            sentiment_category = 'Neutral'
        
        # Generate content
        brand = random.choice(['Our Brand', 'Product X', 'Service Y']) if not keywords else random.choice(keywords)
        content = random.choice(content_templates).format(brand=brand)
        
        # Generate other metrics
        engagement = random.randint(0, 1000)
        reach = random.randint(100, 10000)
        mentions = random.randint(1, 50)
        
        # Location data
        countries = ['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'Japan', 'Brazil']
        cities = ['New York', 'London', 'Toronto', 'Berlin', 'Paris', 'Sydney', 'Tokyo', 'São Paulo']
        
        record = {
            'timestamp': timestamps[i],
            'platform': platform,
            'content': content,
            'sentiment': sentiment_score,
            'sentiment_category': sentiment_category,
            'engagement': engagement,
            'reach': reach,
            'mentions': mentions,
            'author': f"user_{random.randint(1000, 9999)}",
            'country': random.choice(countries),
            'city': random.choice(cities),
            'keywords': [kw.strip() for kw in keywords if kw.strip()] if keywords else [brand],
            'shares': random.randint(0, 100),
            'likes': random.randint(0, 500),
            'comments': random.randint(0, 50),
            'location': f"{random.choice(cities)}, {random.choice(countries)}"
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

def get_real_time_data(platforms=None, sentiment_filter=None, keyword_filter=None, min_engagement=0, limit=25):
    """Generate real-time feed data"""
    
    if platforms is None:
        platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']
    
    if sentiment_filter is None:
        sentiment_filter = ['Positive', 'Negative', 'Neutral']
    
    # Generate real-time posts
    posts = []
    for i in range(limit):
        platform = random.choice(platforms)
        sentiment_score = np.random.normal(0.1, 0.5)
        sentiment_score = max(-1, min(1, sentiment_score))
        
        # Categorize sentiment
        if sentiment_score > 0.2:
            sentiment_category = 'Positive'
        elif sentiment_score < -0.2:
            sentiment_category = 'Negative'
        else:
            sentiment_category = 'Neutral'
        
        # Skip if not in filter
        if sentiment_category not in sentiment_filter:
            continue
        
        engagement = random.randint(0, 1000)
        
        # Skip if below minimum engagement
        if engagement < min_engagement:
            continue
        
        # Generate content
        content_options = [
            "Just discovered this amazing feature! Love it so much 🚀",
            "Having some technical difficulties. Anyone else experiencing this?",
            "Incredible customer service experience today! Thank you team 👏",
            "The new update is game-changing. Highly recommend! ⭐⭐⭐⭐⭐",
            "Could use some improvements but overall satisfied with the service",
            "Best decision I made this year. Absolutely fantastic! 🎉",
            "Disappointed with recent changes. Hope they listen to feedback",
            "Quick and professional response. Impressed! 💯",
            "Been a loyal customer for years. Keep up the great work!",
            "First time user and already impressed. Great onboarding process"
        ]
        
        content = random.choice(content_options)
        
        # Apply keyword filter
        if keyword_filter and keyword_filter.strip():
            if keyword_filter.lower() not in content.lower():
                continue
        
        post = {
            'id': f"post_{random.randint(10000, 99999)}",
            'platform': platform,
            'content': content,
            'author': f"user_{random.randint(1000, 9999)}",
            'timestamp': datetime.now() - timedelta(seconds=random.randint(0, 3600)),
            'sentiment': sentiment_score,
            'sentiment_category': sentiment_category,
            'engagement': engagement,
            'reach': random.randint(1000, 50000),
            'shares': random.randint(0, 100),
            'likes': random.randint(0, 500),
            'comments': random.randint(0, 50),
            'location': f"{random.choice(['New York', 'London', 'Paris', 'Tokyo'])}, {random.choice(['USA', 'UK', 'France', 'Japan'])}",
            'keywords': ['social media', 'monitoring', 'analytics']
        }
        
        posts.append(post)
    
    # Sort by timestamp (newest first)
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return posts

def generate_historical_data(days=30):
    """Generate historical data for trends analysis"""
    
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='H')
    
    data = []
    for date in dates:
        # Simulate daily patterns (higher activity during business hours)
        hour = date.hour
        base_activity = 50
        if 9 <= hour <= 17:  # Business hours
            base_activity = 100
        elif 19 <= hour <= 22:  # Evening peak
            base_activity = 80
        
        # Add some randomness
        mentions = max(0, int(np.random.normal(base_activity, 20)))
        sentiment = np.random.normal(0.1, 0.3)  # Slightly positive bias
        engagement_rate = max(0, np.random.normal(0.05, 0.02))
        
        record = {
            'timestamp': date,
            'mentions': mentions,
            'sentiment': sentiment,
            'engagement_rate': engagement_rate,
            'reach': mentions * random.randint(10, 100)
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

def get_trending_topics(limit=10):
    """Get trending topics/hashtags"""
    
    topics = [
        '#SocialMedia', '#Marketing', '#DigitalTransformation', '#CustomerExperience',
        '#BrandAwareness', '#ContentMarketing', '#Engagement', '#Analytics',
        '#Innovation', '#Technology', '#AI', '#MachineLearning',
        '#DataScience', '#BusinessIntelligence', '#Growth', '#Strategy'
    ]
    
    trending = []
    for topic in random.sample(topics, limit):
        trending.append({
            'topic': topic,
            'mentions': random.randint(50, 1000),
            'growth': random.uniform(-50, 200),  # Percentage growth
            'sentiment': random.uniform(-0.5, 0.8)
        })
    
    # Sort by mentions
    trending.sort(key=lambda x: x['mentions'], reverse=True)
    
    return trending

def get_competitor_data(competitors=None):
    """Generate competitor comparison data"""
    
    if competitors is None:
        competitors = ['Competitor A', 'Competitor B', 'Competitor C', 'Our Brand']
    
    data = []
    for competitor in competitors:
        data.append({
            'name': competitor,
            'mentions': random.randint(100, 1000),
            'sentiment': random.uniform(-0.3, 0.7),
            'engagement_rate': random.uniform(0.02, 0.12),
            'reach': random.randint(10000, 100000),
            'market_share': random.uniform(0.1, 0.4)
        })
    
    return pd.DataFrame(data)

# Utility functions for data processing
def calculate_growth_rate(current, previous):
    """Calculate percentage growth rate"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def categorize_engagement(engagement_rate):
    """Categorize engagement rate"""
    if engagement_rate < 0.02:
        return 'Low'
    elif engagement_rate < 0.05:
        return 'Medium'
    elif engagement_rate < 0.08:
        return 'High'
    else:
        return 'Very High'

def get_platform_demographics():
    """Get demographic data for different platforms"""
    return {
        'Twitter': {
            'age_groups': {'18-24': 25, '25-34': 35, '35-44': 20, '45-54': 15, '55+': 5},
            'gender': {'Male': 52, 'Female': 48},
            'regions': {'North America': 40, 'Europe': 30, 'Asia': 20, 'Other': 10}
        },
        'Facebook': {
            'age_groups': {'18-24': 15, '25-34': 30, '35-44': 25, '45-54': 20, '55+': 10},
            'gender': {'Male': 48, 'Female': 52},
            'regions': {'North America': 35, 'Europe': 25, 'Asia': 25, 'Other': 15}
        },
        'Instagram': {
            'age_groups': {'18-24': 40, '25-34': 35, '35-44': 15, '45-54': 8, '55+': 2},
            'gender': {'Male': 45, 'Female': 55},
            'regions': {'North America': 30, 'Europe': 25, 'Asia': 30, 'Other': 15}
        },
        'LinkedIn': {
            'age_groups': {'18-24': 10, '25-34': 40, '35-44': 30, '45-54': 15, '55+': 5},
            'gender': {'Male': 55, 'Female': 45},
            'regions': {'North America': 45, 'Europe': 30, 'Asia': 15, 'Other': 10}
        }
    }
