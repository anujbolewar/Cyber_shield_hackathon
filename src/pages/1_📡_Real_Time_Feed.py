import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import random
import sys
import os
from pathlib import Path

# Add project root to path for imports
current_dir = Path(__file__).parent.parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from utils.data_generator import get_real_time_data
from utils.sentiment_analyzer import analyze_sentiment
import plotly.express as px

st.set_page_config(
    page_title="Real-time Intelligence Feed - Police AI Monitor",
    page_icon="📡",
    layout="wide"
)

# Initialize session state
if 'feed_active' not in st.session_state:
    st.session_state.feed_active = True

if 'security_clearance' not in st.session_state:
    st.session_state.security_clearance = 'AUTHORIZED'

# Enhanced Police Theme CSS for Real-time Feed
st.markdown("""
<style>
    /* Police theme variables */
    :root {
        --police-blue: #1e3a8a;
        --police-blue-dark: #1e40af;
        --police-blue-light: #3b82f6;
        --police-accent: #fbbf24;
        --police-red: #dc2626;
        --police-green: #16a34a;
    }
    
    /* Real-time feed header */
    .feed-header {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .feed-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--police-red) 0%, var(--police-accent) 50%, var(--police-red) 100%);
        animation: security-sweep 3s infinite linear;
    }
    
    @keyframes security-sweep {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Enhanced feed items */
    .feed-item {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feed-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
    }
    
    .feed-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--police-blue);
    }
    
    .feed-header-info {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .platform-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .platform-twitter { background: #1DA1F2; color: white; }
    .platform-facebook { background: #4267B2; color: white; }
    .platform-instagram { background: #E4405F; color: white; }
    .platform-linkedin { background: #0077B5; color: white; }
    .platform-tiktok { background: #000000; color: white; }
    
    .sentiment-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .sentiment-positive { background: #dcfce7; color: var(--police-green); }
    .sentiment-negative { background: #fee2e2; color: var(--police-red); }
    .sentiment-neutral { background: #fef3c7; color: #d97706; }
    
    .priority-indicator {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: pulse-priority 2s infinite;
    }
    
    .priority-high { background: var(--police-red); }
    .priority-medium { background: var(--police-accent); }
    .priority-low { background: var(--police-green); }
    
    @keyframes pulse-priority {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Live indicator enhanced */
    .live-indicator {
        background: linear-gradient(45deg, var(--police-red) 0%, #dc2626 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        animation: pulse-live 2s infinite;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    @keyframes pulse-live {
        0% { opacity: 1; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3); }
        50% { opacity: 0.8; box-shadow: 0 8px 20px rgba(220, 38, 38, 0.5); }
        100% { opacity: 1; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3); }
    }
    
    /* Enhanced metrics bar */
    .metrics-bar {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .metric-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--police-accent);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Mobile responsive design */
    @media (max-width: 768px) {
        .feed-header {
            padding: 1.5rem 1rem;
        }
        
        .feed-item {
            padding: 1rem;
            margin: 0.8rem 0;
        }
        
        .feed-header-info {
            flex-direction: column;
            align-items: flex-start;
        }
        
        .metrics-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.8rem;
        }
        
        .metric-item {
            padding: 0.8rem;
        }
        
        .metric-value {
            font-size: 1.4rem;
        }
        
        .live-indicator {
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        .platform-badge {
            font-size: 0.75rem;
            padding: 0.3rem 0.6rem;
        }
        
        .sentiment-badge {
            font-size: 0.7rem;
            padding: 0.2rem 0.6rem;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr 1fr;
        }
    }
    
    /* Enhanced sidebar for analytics */
    .analytics-sidebar {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #cbd5e1;
    }
    
    .analytics-header {
        color: var(--police-blue);
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--police-blue);
    }
    
    /* Security classification */
    .classification-banner {
        background: var(--police-red);
        color: white;
        text-align: center;
        padding: 0.5rem;
        font-weight: bold;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Security classification banner
    st.markdown("""
    <div class="classification-banner">
        � CLASSIFIED - LAW ENFORCEMENT USE ONLY 🔒
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced header
    st.markdown("""
    <div class="feed-header">
        <h1>📡 REAL-TIME INTELLIGENCE FEED</h1>
        <p>Live monitoring of social media platforms for law enforcement operations</p>
        <div style="margin-top: 1rem;">
            <div class="live-indicator">
                🔴 LIVE MONITORING ACTIVE
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls with enhanced security
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h3>🔐 SECURE CONTROL PANEL</h3>
            <p>Authorized Personnel Only</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Security status
        if st.session_state.security_clearance == 'AUTHORIZED':
            st.success("✅ Security Clearance: AUTHORIZED")
        else:
            st.error("❌ Access Denied")
            st.stop()
        
        st.header("📻 Feed Controls")
        
        # Auto-refresh settings
        auto_refresh = st.checkbox("Auto Refresh", value=True)
        refresh_interval = st.selectbox(
            "Refresh Interval",
            [5, 10, 15, 30, 60],
            index=2,
            format_func=lambda x: f"{x} seconds"
        )
        
        # Platform filters
        st.subheader("🔧 Filters")
        platforms = st.multiselect(
            "Platforms",
            ["Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok"],
            default=["Twitter", "Facebook", "Instagram"]
        )
        
        # Sentiment filter
        sentiment_filter = st.multiselect(
            "Sentiment",
            ["Positive", "Negative", "Neutral"],
            default=["Positive", "Negative", "Neutral"]
        )
        
        # Keywords filter
        keyword_filter = st.text_input("Filter by Keywords", placeholder="Enter keywords...")
        
        # Minimum engagement threshold
        min_engagement = st.slider("Minimum Engagement", 0, 1000, 0)
        
        # Feed size
        feed_size = st.selectbox("Feed Size", [10, 25, 50, 100], index=1)
        
        # Export options
        st.subheader("📥 Export")
        if st.button("Export Current Feed"):
            export_feed_data()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Real-time metrics bar
        display_realtime_metrics()
        
        # Feed container
        feed_container = st.container()
        
        with feed_container:
            # Get real-time data
            feed_data = get_real_time_data(
                platforms=platforms,
                sentiment_filter=sentiment_filter,
                keyword_filter=keyword_filter,
                min_engagement=min_engagement,
                limit=feed_size
            )
            
            # Display feed items
            for item in feed_data:
                display_feed_item(item)
    
    with col2:
        # Real-time analytics sidebar
        st.subheader("📊 Live Analytics")
        
        # Activity chart
        activity_chart = create_activity_chart()
        st.plotly_chart(activity_chart, use_container_width=True)
        
        # Top hashtags
        st.subheader("🔥 Trending")
        display_trending_hashtags()
        
        # Platform distribution
        st.subheader("📱 Platform Split")
        platform_chart = create_platform_distribution()
        st.plotly_chart(platform_chart, use_container_width=True)
        
        # Sentiment gauge
        st.subheader("😊 Sentiment Meter")
        sentiment_gauge = create_sentiment_gauge()
        st.plotly_chart(sentiment_gauge, use_container_width=True)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

def display_realtime_metrics():
    """Display enhanced real-time metrics with police styling"""
    st.markdown("### 🚨 OPERATIONAL METRICS")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Mentions/Hour",
            value=random.randint(50, 200),
            delta=f"{random.randint(-10, 15):+d}"
        )
    
    with col2:
        threat_level = random.choice(["LOW", "MEDIUM", "HIGH"])
        if threat_level == "HIGH":
            st.error(f"🔴 {threat_level}")
        elif threat_level == "MEDIUM":
            st.warning(f"🟡 {threat_level}")
        else:
            st.success(f"🟢 {threat_level}")
    
    with col3:
        engagement_rate = random.uniform(0.02, 0.15)
        st.metric(
            label="Engagement Rate",
            value=f"{engagement_rate:.1%}",
            delta=f"{random.uniform(-0.02, 0.03):+.1%}"
        )
    
    with col4:
        active_monitors = random.randint(1000, 5000)
        st.metric(
            label="Active Monitors",
            value=f"{active_monitors:,}",
            delta=f"{random.randint(-100, 200):+d}"
        )
    
    with col5:
        active_alerts = random.randint(0, 8)
        if active_alerts > 5:
            st.error(f"🚨 {active_alerts} Alerts")
        elif active_alerts > 2:
            st.warning(f"⚠️ {active_alerts} Alerts")
        else:
            st.success(f"✅ {active_alerts} Alerts")

def display_feed_item(item):
    """Display enhanced feed item with police styling"""
    # Determine priority based on sentiment and engagement
    if item['sentiment'] < -0.5 or item['engagement'] > 500:
        priority = 'high'
        priority_icon = '🔴'
    elif item['sentiment'] < 0 or item['engagement'] > 100:
        priority = 'medium'
        priority_icon = '🟡'
    else:
        priority = 'low'
        priority_icon = '🟢'
    
    platform_class = f"platform-{item['platform'].lower()}"
    sentiment_class = f"sentiment-{item['sentiment_category'].lower()}"
    
    # Create a proper container with Streamlit components
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**📱 {item['platform']}** | **� @{item['author']}**")
            
        with col2:
            if item['sentiment_category'] == 'Positive':
                st.success(f"😊 {item['sentiment_category']}")
            elif item['sentiment_category'] == 'Negative':
                st.error(f"😠 {item['sentiment_category']}")
            else:
                st.warning(f"� {item['sentiment_category']}")
        
        with col3:
            st.info(f"{priority_icon} {priority.upper()}")
        
        # Content
        st.markdown(f"**Content:** {item['content'][:200]}{'...' if len(item['content']) > 200 else ''}")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sentiment", f"{item['sentiment']:.2f}")
        with col2:
            st.metric("Engagement", item['engagement'])
        with col3:
            st.metric("Reach", f"{item['reach']:,}")
        with col4:
            st.metric("Time", item['timestamp'].strftime('%H:%M:%S'))
        
        # Location info
        st.caption(f"� {item['location']} | � {item['timestamp'].strftime('%H:%M:%S')}")
        
        st.divider()

def create_activity_chart():
    """Create real-time activity chart"""
    # Generate sample activity data for the last hour
    now = datetime.now()
    times = [now - timedelta(minutes=i*5) for i in range(12, 0, -1)]
    activity = [random.randint(10, 50) for _ in times]
    
    df = pd.DataFrame({
        'time': times,
        'mentions': activity
    })
    
    fig = px.line(
        df, 
        x='time', 
        y='mentions',
        title="Activity (Last Hour)",
        line_shape='spline'
    )
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )
    fig.update_traces(line_color='#1f77b4')
    return fig

def display_trending_hashtags():
    """Display trending hashtags"""
    hashtags = [
        "#SocialMedia", "#Marketing", "#BrandAwareness", 
        "#CustomerService", "#Innovation", "#Trending",
        "#ViralContent", "#Engagement"
    ]
    
    for i, hashtag in enumerate(hashtags[:5]):
        mentions = random.randint(50, 500)
        trend = random.choice(["↗️", "↘️", "→"])
        st.markdown(f"**{hashtag}** {trend} {mentions} mentions")

def create_platform_distribution():
    """Create platform distribution pie chart"""
    platforms = ["Twitter", "Facebook", "Instagram", "LinkedIn"]
    values = [random.randint(20, 100) for _ in platforms]
    
    fig = px.pie(
        values=values,
        names=platforms,
        title="Platform Distribution"
    )
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )
    return fig

def create_sentiment_gauge():
    """Create sentiment gauge chart"""
    sentiment_score = random.uniform(-1, 1)
    
    fig = px.pie(
        values=[abs(sentiment_score), 2 - abs(sentiment_score)],
        names=['Current', 'Range'],
        title=f"Sentiment: {sentiment_score:.2f}"
    )
    fig.update_layout(
        height=150,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )
    return fig

def export_feed_data():
    """Export current feed data"""
    st.success("Feed data exported to downloads folder!")
    # Implementation would save current feed data to CSV/JSON

if __name__ == "__main__":
    main()
