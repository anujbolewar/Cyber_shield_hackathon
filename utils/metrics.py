"""
Metrics calculation utilities for social media monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_metrics(df):
    """Calculate key metrics from social media data"""
    
    if df.empty:
        return {
            'total_mentions': 0,
            'mentions_change': 0,
            'avg_sentiment': 0,
            'sentiment_change': 0,
            'engagement_rate': 0,
            'engagement_change': 0,
            'total_reach': 0,
            'reach_change': 0
        }
    
    # Calculate current metrics
    total_mentions = df['mentions'].sum() if 'mentions' in df.columns else 0
    avg_sentiment = df['sentiment'].mean() if 'sentiment' in df.columns else 0
    total_engagement = df['engagement'].sum() if 'engagement' in df.columns else 0
    total_reach = df['reach'].sum() if 'reach' in df.columns else 0
    
    # Calculate engagement rate
    engagement_rate = total_engagement / total_reach if total_reach > 0 else 0
    
    # Mock change calculations (would normally compare with previous period)
    mentions_change = np.random.uniform(-0.2, 0.3)  # -20% to +30%
    sentiment_change = np.random.uniform(-0.1, 0.2)  # -0.1 to +0.2
    engagement_change = np.random.uniform(-0.15, 0.25)  # -15% to +25%
    reach_change = np.random.uniform(-0.1, 0.4)  # -10% to +40%
    
    return {
        'total_mentions': total_mentions,
        'mentions_change': mentions_change,
        'avg_sentiment': avg_sentiment,
        'sentiment_change': sentiment_change,
        'engagement_rate': engagement_rate,
        'engagement_change': engagement_change,
        'total_reach': total_reach,
        'reach_change': reach_change
    }

def calculate_engagement_metrics(df):
    """Calculate detailed engagement metrics"""
    
    if df.empty or 'engagement' not in df.columns:
        return {}
    
    metrics = {}
    
    # Basic engagement statistics
    metrics['total_engagement'] = df['engagement'].sum()
    metrics['avg_engagement'] = df['engagement'].mean()
    metrics['median_engagement'] = df['engagement'].median()
    metrics['max_engagement'] = df['engagement'].max()
    
    # Engagement rate by platform
    if 'platform' in df.columns:
        platform_engagement = df.groupby('platform')['engagement'].agg(['sum', 'mean', 'count'])
        metrics['platform_engagement'] = platform_engagement.to_dict()
    
    # Engagement distribution
    if len(df) > 0:
        engagement_quartiles = df['engagement'].quantile([0.25, 0.5, 0.75])
        metrics['engagement_quartiles'] = engagement_quartiles.to_dict()
    
    return metrics

def calculate_sentiment_metrics(df):
    """Calculate sentiment-related metrics"""
    
    if df.empty or 'sentiment' not in df.columns:
        return {}
    
    metrics = {}
    
    # Basic sentiment statistics
    metrics['avg_sentiment'] = df['sentiment'].mean()
    metrics['sentiment_std'] = df['sentiment'].std()
    metrics['sentiment_range'] = df['sentiment'].max() - df['sentiment'].min()
    
    # Sentiment distribution
    if 'sentiment_category' in df.columns:
        sentiment_counts = df['sentiment_category'].value_counts()
        total_posts = len(df)
        
        metrics['sentiment_distribution'] = {
            'positive_pct': sentiment_counts.get('Positive', 0) / total_posts * 100,
            'neutral_pct': sentiment_counts.get('Neutral', 0) / total_posts * 100,
            'negative_pct': sentiment_counts.get('Negative', 0) / total_posts * 100
        }
    
    # Sentiment by platform
    if 'platform' in df.columns:
        platform_sentiment = df.groupby('platform')['sentiment'].agg(['mean', 'count'])
        metrics['platform_sentiment'] = platform_sentiment.to_dict()
    
    return metrics

def calculate_reach_metrics(df):
    """Calculate reach and visibility metrics"""
    
    if df.empty:
        return {}
    
    metrics = {}
    
    # Basic reach statistics
    if 'reach' in df.columns:
        metrics['total_reach'] = df['reach'].sum()
        metrics['avg_reach'] = df['reach'].mean()
        metrics['reach_per_post'] = df['reach'].mean()
    
    # Impressions (if available)
    if 'impressions' in df.columns:
        metrics['total_impressions'] = df['impressions'].sum()
        metrics['avg_impressions'] = df['impressions'].mean()
    
    # Unique reach calculation (mock)
    if 'reach' in df.columns:
        # In reality, this would require more sophisticated deduplication
        metrics['estimated_unique_reach'] = df['reach'].sum() * 0.7  # Assume 30% overlap
    
    return metrics

def calculate_growth_metrics(current_df, previous_df):
    """Calculate growth metrics by comparing two periods"""
    
    if current_df.empty:
        return {}
    
    current_metrics = calculate_metrics(current_df)
    
    if previous_df.empty:
        # If no previous data, return current metrics with zero growth
        growth_metrics = {}
        for key, value in current_metrics.items():
            if 'change' not in key:
                growth_metrics[f"{key}_growth"] = 0
        return growth_metrics
    
    previous_metrics = calculate_metrics(previous_df)
    growth_metrics = {}
    
    # Calculate growth rates
    for key in ['total_mentions', 'avg_sentiment', 'engagement_rate', 'total_reach']:
        if key in current_metrics and key in previous_metrics:
            current_val = current_metrics[key]
            previous_val = previous_metrics[key]
            
            if previous_val != 0:
                growth_rate = (current_val - previous_val) / previous_val * 100
            else:
                growth_rate = 100 if current_val > 0 else 0
            
            growth_metrics[f"{key}_growth"] = growth_rate
    
    return growth_metrics

def calculate_platform_performance(df):
    """Calculate performance metrics by platform"""
    
    if df.empty or 'platform' not in df.columns:
        return {}
    
    platform_metrics = {}
    
    for platform in df['platform'].unique():
        platform_data = df[df['platform'] == platform]
        
        platform_metrics[platform] = {
            'post_count': len(platform_data),
            'total_mentions': platform_data['mentions'].sum() if 'mentions' in df.columns else 0,
            'avg_sentiment': platform_data['sentiment'].mean() if 'sentiment' in df.columns else 0,
            'total_engagement': platform_data['engagement'].sum() if 'engagement' in df.columns else 0,
            'avg_engagement': platform_data['engagement'].mean() if 'engagement' in df.columns else 0,
            'total_reach': platform_data['reach'].sum() if 'reach' in df.columns else 0,
            'engagement_rate': (
                platform_data['engagement'].sum() / platform_data['reach'].sum()
                if 'engagement' in df.columns and 'reach' in df.columns and platform_data['reach'].sum() > 0
                else 0
            )
        }
    
    return platform_metrics

def calculate_temporal_metrics(df):
    """Calculate metrics over time periods"""
    
    if df.empty or 'timestamp' not in df.columns:
        return {}
    
    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    temporal_metrics = {}
    
    # Hourly metrics
    df['hour'] = df['timestamp'].dt.hour
    hourly_activity = df.groupby('hour').agg({
        'mentions': 'sum' if 'mentions' in df.columns else lambda x: len(x),
        'engagement': 'sum' if 'engagement' in df.columns else lambda x: 0,
        'sentiment': 'mean' if 'sentiment' in df.columns else lambda x: 0
    })
    temporal_metrics['hourly'] = hourly_activity.to_dict()
    
    # Daily metrics
    df['date'] = df['timestamp'].dt.date
    daily_activity = df.groupby('date').agg({
        'mentions': 'sum' if 'mentions' in df.columns else lambda x: len(x),
        'engagement': 'sum' if 'engagement' in df.columns else lambda x: 0,
        'sentiment': 'mean' if 'sentiment' in df.columns else lambda x: 0
    })
    temporal_metrics['daily'] = daily_activity.to_dict()
    
    # Peak activity times
    peak_hour = hourly_activity['mentions'].idxmax() if not hourly_activity.empty else 0
    temporal_metrics['peak_hour'] = peak_hour
    
    return temporal_metrics

def calculate_content_metrics(df):
    """Calculate content-related metrics"""
    
    if df.empty:
        return {}
    
    content_metrics = {}
    
    # Content length analysis (if content is available)
    if 'content' in df.columns:
        df['content_length'] = df['content'].str.len()
        content_metrics['avg_content_length'] = df['content_length'].mean()
        content_metrics['content_length_std'] = df['content_length'].std()
    
    # Top performing content
    if 'engagement' in df.columns:
        top_content = df.nlargest(5, 'engagement')
        content_metrics['top_performing'] = top_content[['content', 'engagement']].to_dict('records')
    
    # Content type analysis (mock - would need actual content classification)
    content_types = ['text', 'image', 'video', 'link']
    type_distribution = {ct: np.random.randint(10, 100) for ct in content_types}
    content_metrics['content_type_distribution'] = type_distribution
    
    return content_metrics

def calculate_influence_metrics(df):
    """Calculate influence and reach metrics"""
    
    if df.empty:
        return {}
    
    influence_metrics = {}
    
    # Author influence (mock - would need actual follower data)
    if 'author' in df.columns:
        author_stats = df.groupby('author').agg({
            'engagement': 'sum' if 'engagement' in df.columns else lambda x: 0,
            'reach': 'sum' if 'reach' in df.columns else lambda x: 0
        })
        
        # Top influencers
        top_authors = author_stats.nlargest(5, 'engagement')
        influence_metrics['top_influencers'] = top_authors.to_dict('index')
    
    # Viral content detection
    if 'engagement' in df.columns and 'reach' in df.columns:
        df['virality_score'] = df['engagement'] / (df['reach'] + 1)  # +1 to avoid division by zero
        viral_threshold = df['virality_score'].quantile(0.9)  # Top 10%
        viral_content = df[df['virality_score'] > viral_threshold]
        influence_metrics['viral_content_count'] = len(viral_content)
        influence_metrics['avg_virality_score'] = df['virality_score'].mean()
    
    return influence_metrics

def calculate_geographical_metrics(df):
    """Calculate geographical distribution metrics"""
    
    if df.empty:
        return {}
    
    geo_metrics = {}
    
    # Country distribution
    if 'country' in df.columns:
        country_stats = df.groupby('country').agg({
            'mentions': 'sum' if 'mentions' in df.columns else lambda x: len(x),
            'sentiment': 'mean' if 'sentiment' in df.columns else lambda x: 0,
            'engagement': 'sum' if 'engagement' in df.columns else lambda x: 0
        })
        geo_metrics['country_distribution'] = country_stats.to_dict()
        
        # Top countries
        top_countries = country_stats.nlargest(5, 'mentions')
        geo_metrics['top_countries'] = top_countries.index.tolist()
    
    # City distribution
    if 'city' in df.columns:
        city_stats = df.groupby('city').agg({
            'mentions': 'sum' if 'mentions' in df.columns else lambda x: len(x),
            'engagement': 'sum' if 'engagement' in df.columns else lambda x: 0
        })
        geo_metrics['city_distribution'] = city_stats.to_dict()
    
    return geo_metrics

def calculate_competitive_metrics(df, competitor_data=None):
    """Calculate competitive analysis metrics"""
    
    metrics = {}
    
    # Market share calculation (mock)
    if competitor_data is not None:
        total_mentions = sum(competitor_data.values())
        our_mentions = df['mentions'].sum() if 'mentions' in df.columns and not df.empty else 0
        
        market_share = our_mentions / (total_mentions + our_mentions) * 100 if (total_mentions + our_mentions) > 0 else 0
        metrics['market_share'] = market_share
        
        # Competitive positioning
        metrics['competitive_ranking'] = calculate_competitive_ranking(our_mentions, competitor_data)
    
    # Share of voice
    if not df.empty and 'mentions' in df.columns:
        total_industry_mentions = df['mentions'].sum() * 5  # Mock total industry
        share_of_voice = (df['mentions'].sum() / total_industry_mentions) * 100
        metrics['share_of_voice'] = share_of_voice
    
    return metrics

def calculate_competitive_ranking(our_mentions, competitor_data):
    """Calculate competitive ranking based on mentions"""
    
    all_mentions = list(competitor_data.values()) + [our_mentions]
    all_mentions.sort(reverse=True)
    
    our_rank = all_mentions.index(our_mentions) + 1
    total_competitors = len(all_mentions)
    
    return {
        'rank': our_rank,
        'total_competitors': total_competitors,
        'percentile': ((total_competitors - our_rank) / total_competitors) * 100
    }

def calculate_trend_metrics(df, periods=7):
    """Calculate trend analysis metrics"""
    
    if df.empty or 'timestamp' not in df.columns:
        return {}
    
    # Ensure timestamp is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    trend_metrics = {}
    
    # Create time-based groupings
    df['date'] = df['timestamp'].dt.date
    daily_metrics = df.groupby('date').agg({
        'mentions': 'sum' if 'mentions' in df.columns else lambda x: len(x),
        'sentiment': 'mean' if 'sentiment' in df.columns else lambda x: 0,
        'engagement': 'sum' if 'engagement' in df.columns else lambda x: 0
    })
    
    # Calculate trends (simple linear regression slope)
    if len(daily_metrics) >= 2:
        for metric in ['mentions', 'sentiment', 'engagement']:
            if metric in daily_metrics.columns:
                values = daily_metrics[metric].values
                x = np.arange(len(values))
                slope = np.polyfit(x, values, 1)[0]
                trend_metrics[f"{metric}_trend"] = 'increasing' if slope > 0 else 'decreasing'
                trend_metrics[f"{metric}_slope"] = slope
    
    return trend_metrics
