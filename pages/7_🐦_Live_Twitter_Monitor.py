#!/usr/bin/env python3
"""
🐦 LIVE TWITTER MONITORING - STREAMLIT INTERFACE
Real-time Twitter monitoring dashboard for law enforcement
Features: Live stream, sentiment analysis, bot detection, geographic clustering
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
import sys
import os

# Add the utils directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

try:
    from twitter_monitor import LiveTwitterMonitor, TweetData
except ImportError:
    st.error("❌ Could not import Twitter monitoring modules. Please ensure all dependencies are installed.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Live Twitter Monitor",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'twitter_monitor' not in st.session_state:
        st.session_state.twitter_monitor = None
    if 'monitoring_active' not in st.session_state:
        st.session_state.monitoring_active = False
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

def get_twitter_theme_css(dark_mode=False):
    """Generate CSS based on theme mode for Twitter monitor"""
    if dark_mode:
        return """
<style>
    /* Dark Mode Theme for Twitter Monitor */
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --twitter-blue: #1da1f2;
        --twitter-dark: #1a91da;
        --border-color: #475569;
    }
    
    .main .block-container {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Twitter header - Dark */
    .twitter-header {
        background: linear-gradient(90deg, #1da1f2 0%, #1a91da 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
    }
    
    /* Tweet cards - Dark */
    .tweet-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: var(--text-primary);
    }
    
    /* Sidebar - Dark */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        color: var(--text-primary);
    }
    
    /* Buttons - Dark */
    .stButton > button {
        background: linear-gradient(135deg, var(--twitter-blue) 0%, var(--twitter-dark) 100%);
        color: white;
        border: 1px solid var(--twitter-blue);
    }
    
    /* Input fields - Dark */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    /* Metrics - Dark */
    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        color: var(--text-primary);
    }
</style>
"""
    else:
        return """
<style>
    /* Light Mode Theme for Twitter Monitor */
    .twitter-header {
        background: linear-gradient(90deg, #1da1f2 0%, #1a91da 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .tweet-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
"""

def load_twitter_data(db_path: str) -> pd.DataFrame:
    """Load Twitter data from database"""
    try:
        if not Path(db_path).exists():
            return pd.DataFrame()
        
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            id, text, author_username, created_at, location,
            latitude, longitude, retweet_count, like_count,
            reply_count, quote_count, sentiment_score,
            threat_level, bot_probability, engagement_velocity,
            keywords_matched, processed_at
        FROM tweets 
        ORDER BY created_at DESC 
        LIMIT 1000
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['processed_at'] = pd.to_datetime(df['processed_at'])
            df['keywords_matched'] = df['keywords_matched'].apply(
                lambda x: json.loads(x) if x else []
            )
        
        return df
        
    except Exception as e:
        st.error(f"Error loading Twitter data: {str(e)}")
        return pd.DataFrame()

def load_alerts_data(db_path: str) -> pd.DataFrame:
    """Load alerts data from database"""
    try:
        if not Path(db_path).exists():
            return pd.DataFrame()
        
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            a.id, a.tweet_id, a.alert_type, a.priority,
            a.message, a.created_at, a.acknowledged,
            t.text, t.author_username
        FROM twitter_alerts a
        LEFT JOIN tweets t ON a.tweet_id = t.id
        ORDER BY a.created_at DESC
        LIMIT 500
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at'])
        
        return df
        
    except Exception as e:
        st.error(f"Error loading alerts data: {str(e)}")
        return pd.DataFrame()

def load_geo_clusters(db_path: str) -> pd.DataFrame:
    """Load geographic clusters data"""
    try:
        if not Path(db_path).exists():
            return pd.DataFrame()
        
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            cluster_name, center_lat, center_lng, 
            radius_km, tweet_count, threat_score,
            created_at, updated_at
        FROM geo_clusters
        ORDER BY threat_score DESC, tweet_count DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading geo clusters: {str(e)}")
        return pd.DataFrame()

def create_sentiment_timeline(df: pd.DataFrame) -> go.Figure:
    """Create sentiment analysis timeline"""
    if df.empty:
        return go.Figure()
    
    # Group by hour and calculate average sentiment
    df_hourly = df.set_index('created_at').resample('1H').agg({
        'sentiment_score': 'mean',
        'id': 'count'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Average Sentiment Score', 'Tweet Volume'],
        vertical_spacing=0.1
    )
    
    # Sentiment timeline
    fig.add_trace(
        go.Scatter(
            x=df_hourly['created_at'],
            y=df_hourly['sentiment_score'],
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(color='blue'),
            hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Tweet volume
    fig.add_trace(
        go.Bar(
            x=df_hourly['created_at'],
            y=df_hourly['id'],
            name='Tweet Count',
            marker_color='lightblue',
            hovertemplate='<b>%{x}</b><br>Tweets: %{y}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_text="Sentiment Analysis Timeline"
    )
    
    return fig

def create_threat_level_chart(df: pd.DataFrame) -> go.Figure:
    """Create threat level distribution chart"""
    if df.empty:
        return go.Figure()
    
    threat_counts = df['threat_level'].value_counts()
    
    colors = {
        'LOW': '#28a745',
        'MEDIUM': '#ffc107', 
        'HIGH': '#fd7e14',
        'CRITICAL': '#dc3545'
    }
    
    fig = go.Figure(data=[
        go.Pie(
            labels=threat_counts.index,
            values=threat_counts.values,
            marker=dict(colors=[colors.get(level, '#6c757d') for level in threat_counts.index]),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Threat Level Distribution",
        height=300
    )
    
    return fig

def create_geographic_map(df: pd.DataFrame) -> go.Figure:
    """Create geographic distribution map"""
    if df.empty or df[['latitude', 'longitude']].isna().all().all():
        return go.Figure()
    
    # Filter out tweets without coordinates
    geo_df = df.dropna(subset=['latitude', 'longitude'])
    
    if geo_df.empty:
        return go.Figure()
    
    # Color mapping for threat levels
    color_map = {
        'LOW': '#28a745',
        'MEDIUM': '#ffc107',
        'HIGH': '#fd7e14', 
        'CRITICAL': '#dc3545'
    }
    
    fig = go.Figure()
    
    for threat_level in geo_df['threat_level'].unique():
        threat_data = geo_df[geo_df['threat_level'] == threat_level]
        
        fig.add_trace(go.Scattermapbox(
            lat=threat_data['latitude'],
            lon=threat_data['longitude'],
            mode='markers',
            marker=dict(
                size=8,
                color=color_map.get(threat_level, '#6c757d'),
                opacity=0.7
            ),
            text=threat_data['text'].str[:100] + '...',
            name=f'{threat_level} ({len(threat_data)})',
            hovertemplate='<b>%{text}</b><br>Location: %{lat:.4f}, %{lon:.4f}<br>Threat: ' + threat_level + '<extra></extra>'
        ))
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=20.5937, lon=78.9629),  # Center of India
            zoom=4
        ),
        height=500,
        title="Geographic Distribution of Tweets"
    )
    
    return fig

def create_bot_detection_chart(df: pd.DataFrame) -> go.Figure:
    """Create bot detection analysis chart"""
    if df.empty:
        return go.Figure()
    
    # Create bot probability bins
    df['bot_category'] = pd.cut(
        df['bot_probability'], 
        bins=[0, 0.3, 0.7, 1.0], 
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    
    bot_counts = df['bot_category'].value_counts()
    
    colors = ['#28a745', '#ffc107', '#dc3545']
    
    fig = go.Figure(data=[
        go.Bar(
            x=bot_counts.index,
            y=bot_counts.values,
            marker_color=colors[:len(bot_counts)],
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Bot Detection Analysis",
        xaxis_title="Bot Risk Level",
        yaxis_title="Number of Tweets",
        height=300
    )
    
    return fig

def display_recent_tweets(df: pd.DataFrame, limit: int = 10):
    """Display recent tweets in a formatted table"""
    if df.empty:
        st.info("No tweets to display")
        return
    
    recent_tweets = df.head(limit)
    
    for idx, tweet in recent_tweets.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Tweet content
                st.markdown(f"**@{tweet['author_username']}**")
                st.write(tweet['text'][:200] + ("..." if len(tweet['text']) > 200 else ""))
                
                # Keywords
                if tweet['keywords_matched']:
                    keywords = ", ".join(tweet['keywords_matched'][:5])
                    st.caption(f"🔍 Keywords: {keywords}")
            
            with col2:
                # Threat level with color
                threat_colors = {
                    'LOW': 'green',
                    'MEDIUM': 'orange', 
                    'HIGH': 'red',
                    'CRITICAL': 'darkred'
                }
                st.markdown(f"**Threat:** :{threat_colors.get(tweet['threat_level'], 'gray')}[{tweet['threat_level']}]")
                st.write(f"**Sentiment:** {tweet['sentiment_score']:.2f}")
                st.write(f"**Bot Prob:** {tweet['bot_probability']:.2f}")
            
            with col3:
                # Engagement metrics
                st.metric("Likes", tweet['like_count'])
                st.metric("Retweets", tweet['retweet_count'])
                st.write(f"📍 {tweet['location'] or 'Unknown'}")
            
            st.divider()

def display_alerts(alerts_df: pd.DataFrame, limit: int = 10):
    """Display recent alerts"""
    if alerts_df.empty:
        st.info("No alerts to display")
        return
    
    recent_alerts = alerts_df.head(limit)
    
    for idx, alert in recent_alerts.iterrows():
        priority_colors = {
            'LOW': 'blue',
            'MEDIUM': 'orange',
            'HIGH': 'red',
            'CRITICAL': 'darkred'
        }
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"**🚨 {alert['alert_type'].replace('_', ' ').title()}**")
                st.write(alert['message'])
                if alert['text']:
                    st.caption(f"Tweet: {alert['text'][:150]}...")
            
            with col2:
                st.markdown(f"**Priority:** :{priority_colors.get(alert['priority'], 'gray')}[{alert['priority']}]")
                st.write(f"**Time:** {alert['created_at'].strftime('%H:%M:%S')}")
                st.write(f"**User:** @{alert['author_username'] or 'Unknown'}")
            
            st.divider()

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Apply theme CSS
    st.markdown(get_twitter_theme_css(False), unsafe_allow_html=True)
    
    # Header
    header_style = "twitter-header" if not st.session_state.dark_mode else "twitter-header"
    st.markdown(f"""
    <div class="{header_style}">
        <h1 style="color: white; margin: 0; display: flex; align-items: center;">
            🐦 Live Twitter Monitoring System
        </h1>
        <p style="color: #E1E8ED; margin: 0.5rem 0 0 0;">Real-time Twitter monitoring for law enforcement with AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        
        st.header("🔧 Monitor Controls")
        
        # API Configuration
        with st.expander("🔑 API Configuration", expanded=False):
            bearer_token = st.text_input(
                "Twitter Bearer Token",
                value="demo_token",
                type="password",
                help="Enter your Twitter API v2 Bearer Token"
            )
            
            if st.button("💾 Save Configuration"):
                st.success("Configuration saved!")
        
        # Monitor Control
        st.subheader("📡 Monitoring Status")
        
        if not st.session_state.monitoring_active:
            if st.button("🚀 Start Monitoring", type="primary"):
                with st.spinner("Starting Twitter monitoring..."):
                    st.session_state.twitter_monitor = LiveTwitterMonitor(bearer_token)
                    if st.session_state.twitter_monitor.start_monitoring():
                        st.session_state.monitoring_active = True
                        st.success("✅ Monitoring started!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to start monitoring")
        else:
            st.success("✅ Monitoring Active")
            if st.button("🛑 Stop Monitoring", type="secondary"):
                if st.session_state.twitter_monitor:
                    st.session_state.twitter_monitor.stop_monitoring()
                st.session_state.monitoring_active = False
                st.session_state.twitter_monitor = None
                st.info("🛑 Monitoring stopped")
                st.rerun()
        
        # Auto-refresh toggle
        st.subheader("🔄 Auto Refresh")
        st.session_state.auto_refresh = st.toggle("Enable Auto Refresh", value=st.session_state.auto_refresh)
        
        refresh_interval = 10  # Default refresh interval
        if st.session_state.auto_refresh:
            refresh_interval = st.selectbox(
                "Refresh Interval",
                options=[5, 10, 30, 60],
                index=1,
                format_func=lambda x: f"{x} seconds"
            )
        
        # Manual refresh
        if st.button("🔄 Refresh Now"):
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        # Filters
        st.subheader("🔍 Filters")
        
        threat_filter = st.multiselect(
            "Threat Levels",
            options=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            default=["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        )
        
        time_filter = st.selectbox(
            "Time Range",
            options=["Last 1 Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days"],
            index=2
        )
        
        # Export options
        st.subheader("📤 Export Data")
        if st.button("💾 Export to CSV"):
            # Get current data
            if st.session_state.twitter_monitor:
                db_path = st.session_state.twitter_monitor.db_path
                df = load_twitter_data(db_path)
                if not df.empty:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name=f"twitter_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
    
    # Main content area
    if not st.session_state.monitoring_active:
        # Show setup instructions
        st.info("👆 Click 'Start Monitoring' in the sidebar to begin live Twitter monitoring")
        
        st.markdown("""
        ## 🐦 Live Twitter Monitoring Features
        
        ### 📡 **Real-time Stream Processing**
        - Stream tweets using Twitter API v2
        - Filter by India-related keywords
        - Process thousands of tweets per minute
        
        ### 🧠 **AI-Powered Analysis**
        - **Sentiment Analysis**: Detect positive, negative, and threatening content
        - **Bot Detection**: Identify automated accounts and bots
        - **Threat Assessment**: Classify content by threat level
        
        ### 🗺️ **Geographic Intelligence**
        - **Location Tracking**: Monitor tweets by geographic location
        - **Clustering Analysis**: Identify hotspots of activity
        - **Regional Monitoring**: Focus on specific areas of interest
        
        ### 🚨 **Automatic Alerting**
        - **Real-time Alerts**: Immediate notifications for high-priority content
        - **Threat Detection**: Automatic escalation of dangerous content
        - **Evidence Capture**: Screenshot and metadata preservation
        
        ### 📊 **Advanced Analytics**
        - **Engagement Velocity**: Track viral content spread
        - **Trend Analysis**: Identify emerging patterns
        - **Performance Metrics**: Monitor system effectiveness
        """)
        
        # Show demo data
        st.subheader("📊 Demo Dashboard")
        st.info("This is sample data. Start monitoring to see live Twitter data.")
        
        # Create demo data
        demo_data = {
            'Tweets Processed': 1247,
            'High Threat Alerts': 23,
            'Bot Accounts Detected': 156,
            'Geographic Clusters': 8
        }
        
        col1, col2, col3, col4 = st.columns(4)
        for i, (metric, value) in enumerate(demo_data.items()):
            with [col1, col2, col3, col4][i]:
                st.metric(metric, value)
        
        return
    
    # Load data
    if st.session_state.twitter_monitor:
        db_path = st.session_state.twitter_monitor.db_path
        df = load_twitter_data(db_path)
        alerts_df = load_alerts_data(db_path)
        geo_df = load_geo_clusters(db_path)
        
        # Get monitoring statistics
        stats = st.session_state.twitter_monitor.get_monitoring_stats()
    else:
        df = pd.DataFrame()
        alerts_df = pd.DataFrame()
        geo_df = pd.DataFrame()
        stats = {}
    
    # Apply filters
    if not df.empty:
        # Threat level filter
        if threat_filter:
            df = df[df['threat_level'].isin(threat_filter)]
        
        # Time filter
        now = datetime.now()
        time_delta_map = {
            "Last 1 Hour": timedelta(hours=1),
            "Last 6 Hours": timedelta(hours=6),
            "Last 24 Hours": timedelta(days=1),
            "Last 7 Days": timedelta(days=7)
        }
        
        time_delta = time_delta_map.get(time_filter, timedelta(days=1))
        cutoff_time = now - time_delta
        df = df[df['created_at'] >= cutoff_time]
    
    # Display key metrics
    st.subheader("📊 Live Monitoring Dashboard")
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Tweets Processed",
                stats.get('total_tweets_processed', 0),
                delta=len(df) if not df.empty else 0
            )
        
        with col2:
            st.metric(
                "Recent Alerts (1h)",
                stats.get('recent_alerts_1h', 0)
            )
        
        with col3:
            st.metric(
                "High Bot Probability",
                stats.get('high_bot_probability_tweets', 0)
            )
        
        with col4:
            st.metric(
                "Geographic Clusters",
                stats.get('geographic_clusters', 0)
            )
    
    # Charts and visualizations
    if not df.empty:
        # Row 1: Sentiment and Threat Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_fig = create_sentiment_timeline(df)
            st.plotly_chart(sentiment_fig, use_container_width=True)
        
        with col2:
            threat_fig = create_threat_level_chart(df)
            st.plotly_chart(threat_fig, use_container_width=True)
        
        # Row 2: Geographic and Bot Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            geo_fig = create_geographic_map(df)
            st.plotly_chart(geo_fig, use_container_width=True)
        
        with col2:
            bot_fig = create_bot_detection_chart(df)
            st.plotly_chart(bot_fig, use_container_width=True)
    
    # Tabs for detailed views
    tab1, tab2, tab3, tab4 = st.tabs(["🐦 Recent Tweets", "🚨 Alerts", "🗺️ Geographic Clusters", "📈 Analytics"])
    
    with tab1:
        st.subheader("🐦 Recent Tweets")
        if not df.empty:
            # Search functionality
            search_term = st.text_input("🔍 Search tweets", placeholder="Enter keywords...")
            if search_term:
                search_df = df[df['text'].str.contains(search_term, case=False, na=False)]
                st.info(f"Found {len(search_df)} tweets matching '{search_term}'")
                display_recent_tweets(search_df, limit=20)
            else:
                display_recent_tweets(df, limit=20)
        else:
            st.info("No tweets to display. Start monitoring to see live data.")
    
    with tab2:
        st.subheader("🚨 Recent Alerts")
        if not alerts_df.empty:
            # Filter alerts by priority
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                default=["MEDIUM", "HIGH", "CRITICAL"]
            )
            
            filtered_alerts = alerts_df[alerts_df['priority'].isin(priority_filter)]
            display_alerts(filtered_alerts, limit=15)
        else:
            st.info("No alerts to display.")
    
    with tab3:
        st.subheader("🗺️ Geographic Clusters")
        if not geo_df.empty:
            st.dataframe(
                geo_df[['cluster_name', 'center_lat', 'center_lng', 'tweet_count', 'threat_score']],
                use_container_width=True
            )
        else:
            st.info("No geographic clusters detected yet.")
    
    with tab4:
        st.subheader("📈 Advanced Analytics")
        
        if not df.empty:
            # Engagement analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top Engaging Tweets**")
                top_engaging = df.nlargest(5, 'engagement_velocity')[['text', 'engagement_velocity', 'author_username']]
                for idx, tweet in top_engaging.iterrows():
                    st.write(f"**@{tweet['author_username']}** ({tweet['engagement_velocity']:.1f} eng/min)")
                    st.caption(tweet['text'][:100] + "...")
                    st.divider()
            
            with col2:
                st.markdown("**Keyword Analysis**")
                # Flatten keywords
                all_keywords = []
                for keywords in df['keywords_matched']:
                    all_keywords.extend(keywords)
                
                if all_keywords:
                    keyword_counts = pd.Series(all_keywords).value_counts().head(10)
                    st.bar_chart(keyword_counts)
                else:
                    st.info("No keywords detected yet.")
        else:
            st.info("Start monitoring to see analytics.")
    
    # Auto-refresh logic for real-time updates
    if st.session_state.auto_refresh and st.session_state.monitoring_active:
        # Use Streamlit's native auto-refresh
        time.sleep(0.1)  # Small delay to prevent too frequent updates
        st.rerun()

if __name__ == "__main__":
    main()
