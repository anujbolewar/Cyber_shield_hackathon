import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import json
import random
import sys
import os
from pathlib import Path

# Add project root to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

# Import modules with new structure
from utils.data_generator import generate_sample_data, get_real_time_data
from core.alerts import check_alerts, display_alerts
from utils.metrics import calculate_metrics

# Import fallback integration
try:
    from utils.fallback_integration import get_fallback_integration
    FALLBACK_AVAILABLE = True
except ImportError:
    print("Warning: Fallback system not available")
    FALLBACK_AVAILABLE = False

# Security and utility functions
def check_security_status():
    """Check system security status"""
    # Simulate security checks
    import random
    return random.random() > 0.1  # 90% chance system is secure

def display_security_warning():
    """Display security warning if system is compromised"""
    st.markdown("""
    <div class="security-banner">
        🚨 SECURITY ALERT: Unauthorized access detected. System temporarily locked.
        Contact system administrator immediately.
    </div>
    """, unsafe_allow_html=True)
    
    st.error("❌ Access Denied - Security protocols activated")
    st.stop()

def display_simple_login():
    """Display simplified login interface"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.4);
    ">
        <h1>🚓 POLICE AI MONITOR</h1>
        <h2>🔒 SECURE ACCESS REQUIRED</h2>
        <p style="font-size: 1.1rem; margin: 1rem 0;">Authorized Law Enforcement Personnel Only</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("simple_login"):
            st.subheader("🔐 Authentication")
            
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("🔓 SECURE LOGIN", use_container_width=True)
            
            if submitted:
                # Simple authentication (in production, use secure authentication)
                if username and password:
                    if authenticate_simple_user(username, password):
                        st.session_state.user_authenticated = True
                        st.session_state.current_user = username
                        st.session_state.session_start = datetime.now()
                        st.session_state.redirect_to_dashboard = True
                        st.success("✅ Authentication successful! Redirecting to Dashboard...")
                        time.sleep(0.5)
                        st.rerun()  # Trigger rerun to activate redirect
                    else:
                        st.error("❌ Invalid credentials. Access denied.")
                        if 'failed_attempts' not in st.session_state:
                            st.session_state.failed_attempts = 0
                        st.session_state.failed_attempts += 1
                        
                        if st.session_state.failed_attempts >= 3:
                            st.error("🚨 Multiple failed attempts detected. System locked for security.")
                else:
                    st.warning("⚠️ Please enter both username and password.")
        
        # Demo credentials info
        with st.expander("📋 Demo Credentials", expanded=False):
            st.markdown("""
            **For demonstration purposes:**
            - Username: `officer1` | Password: `demo123`
            - Username: `detective1` | Password: `demo456`
            - Username: `admin` | Password: `admin789`
            
            ⚠️ **Security Notice:** In production, use secure authentication systems.
            """)

def authenticate_simple_user(username, password):
    """Simple authentication function for demo"""
    demo_users = {
        "officer1": "demo123",
        "detective1": "demo456", 
        "admin": "admin789",
        "demo": "demo"
    }
    
    return username in demo_users and demo_users[username] == password

# Page configuration
st.set_page_config(
    page_title="Police AI Monitor",
    page_icon="🚓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://police-ai-monitor.help',
        'Report a bug': 'https://police-ai-monitor.bugs',
        'About': "# Police AI Monitor\nAdvanced social media monitoring for law enforcement."
    }
)

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Initialize session state for API keys and security
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'openai': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False},
        'twitter': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False},
        'facebook': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False},
        'telegram': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False},
        'news_api': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False},
        'reddit': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False},
        'youtube': {'key': '', 'status': 'disconnected', 'last_tested': None, 'is_demo': False}
    }

if 'security_level' not in st.session_state:
    st.session_state.security_level = 'HIGH'

if 'system_status' not in st.session_state:
    st.session_state.system_status = {
        'api_status': 'OPERATIONAL',
        'data_feed': 'ACTIVE',
        'alerts': 'MONITORING',
        'security': 'SECURE'
    }

if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False

# Professional Police Theme CSS with Dark Mode Support
def get_theme_css(dark_mode=False):
    """Generate CSS based on theme mode"""
    if dark_mode:
        return """
<style>
    /* Dark Mode Theme - Police Style */
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --police-blue: #3b82f6;
        --police-blue-dark: #1d4ed8;
        --police-blue-light: #60a5fa;
        --police-accent: #fbbf24;
        --police-red: #ef4444;
        --police-green: #22c55e;
        --border-color: #475569;
    }
    
    /* Global dark theme overrides */
    .main .block-container {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Sidebar dark styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        color: var(--text-primary);
    }
    
    /* Header styling - Dark */
    .police-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }
    
    /* Metric cards - Dark */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid var(--police-blue);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Status indicators - Dark */
    .status-indicator {
        background: rgba(51, 65, 85, 0.8);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    /* Buttons - Dark */
    .stButton > button {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        border: 1px solid var(--police-blue);
    }
    
    /* Input fields - Dark */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    /* Dataframes and tables - Dark */
    .dataframe {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }
    
    /* Expander - Dark */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    /* Tabs - Dark */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--police-blue);
        color: white;
    }
    
    /* Plotly charts - Dark */
    .js-plotly-plot {
        background-color: var(--bg-secondary) !important;
    }
    
    /* Common elements */
    .police-badge {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid var(--police-blue);
    }
    
    .status-bar {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid var(--border-color);
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--police-blue) 100%);
        border: 1px solid var(--border-color);
    }
</style>
"""
    else:
        return """
<style>
    /* Light Mode Theme - Police Style */
    :root {
        --police-blue: #1e3a8a;
        --police-blue-dark: #1e40af;
        --police-blue-light: #3b82f6;
        --police-accent: #fbbf24;
        --police-red: #dc2626;
        --police-green: #16a34a;
        --police-gray: #374151;
        --police-light-gray: #f3f4f6;
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Header styling */
    .police-header {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .police-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--police-accent) 0%, var(--police-red) 50%, var(--police-accent) 100%);
    }
    
    .police-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Status indicators */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .status-operational { border-left: 3px solid var(--police-green); }
    .status-warning { border-left: 3px solid var(--police-accent); }
    .status-critical { border-left: 3px solid var(--police-red); }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, white 0%, var(--police-light-gray) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid var(--police-blue);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--police-blue-dark) 0%, var(--police-blue) 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-light) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
    }
</style>
"""

st.markdown(get_theme_css(False), unsafe_allow_html=True)

def main():
    # Initialize fallback integration
    if FALLBACK_AVAILABLE:
        fallback_integration = get_fallback_integration()
        fallback_status = fallback_integration.get_system_status()
    else:
        fallback_integration = None
        fallback_status = {'mode': 'UNAVAILABLE', 'health': 0}
    
    # Check if user is authenticated and should be redirected
    if st.session_state.get('user_authenticated', False) and st.session_state.get('redirect_to_dashboard', True):
        try:
            st.session_state.redirect_to_dashboard = False  # Prevent redirect loop
            st.switch_page("pages/0_🏠_Dashboard.py")
        except:
            pass  # Continue with normal flow if redirect fails
    
    # Inject mobile responsive CSS
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        
        .police-header {
            padding: 1rem !important;
            text-align: center;
        }
        
        .status-bar {
            flex-direction: column !important;
            align-items: stretch !important;
        }
        
        .status-indicator {
            justify-content: center !important;
            text-align: center !important;
            margin: 0.25rem 0 !important;
        }
        
        .dashboard-grid {
            grid-template-columns: 1fr 1fr !important;
            gap: 0.5rem !important;
        }
        
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
    }
    
    @media (max-width: 480px) {
        .dashboard-grid {
            grid-template-columns: 1fr !important;
        }
        
        .police-badge {
            font-size: 0.8rem !important;
            padding: 0.3rem 0.8rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Security check with authentication requirement
    try:
        # Simple authentication check
        if not st.session_state.get('user_authenticated', False):
            display_simple_login()
            return
        
        # If authenticated, automatically redirect to dashboard
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(22, 163, 74, 0.4);
        ">
            <h1>✅ AUTHENTICATION SUCCESSFUL</h1>
            <h2>🚀 ACCESSING DASHBOARD</h2>
            <p style="font-size: 1.1rem; margin: 1rem 0;">Welcome to the Police AI Monitor System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Immediate redirect to dashboard
        try:
            st.switch_page("pages/0_🏠_Dashboard.py")
        except Exception as e:
            # If switch_page fails, show manual navigation options
            st.warning("Automatic redirect failed. Please use the options below:")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 GO TO DASHBOARD", type="primary", use_container_width=True):
                    try:
                        st.switch_page("pages/0_🏠_Dashboard.py")
                    except:
                        st.error("Please manually navigate to the '🏠 Dashboard' page in the sidebar.")
            
            st.markdown("""
            <div style="
                background: rgba(59, 130, 246, 0.1);
                border: 2px solid #3b82f6;
                color: #1e40af;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 2rem 0;
                text-align: center;
            ">
                <h3>🏠 DASHBOARD ACCESS</h3>
                <p>Please manually navigate to the <strong>"🏠 Dashboard"</strong> page in the sidebar.</p>
                <p>The dashboard provides access to all system features including real-time monitoring, analytics, and more.</p>
            </div>
            """, unsafe_allow_html=True)
        
        if not check_security_status():
            display_security_warning()
            return
    except Exception as e:
        st.error(f"Security system error: {str(e)}")
        return
    
    # Determine fallback status for display
    fallback_icon = "🛡️" if fallback_status.get('health', 0) > 50 else "⚠️"
    fallback_text = f"Fallback: {fallback_status.get('mode', 'N/A')}"
    
    # Police header with badge
    st.markdown("""
    <div class="police-header">
        <div class="police-badge">
            🚓 POLICE AI MONITOR SYSTEM
        </div>
        <h1>🔍 Advanced Social Media Intelligence Platform</h1>
        <p>Real-time monitoring and analysis for law enforcement operations</p>
        
        <div class="status-bar">
            <div class="status-indicator status-operational">
                <span class="loading-spinner"></span>
                <span>System Status: {}</span>
            </div>
            <div class="status-indicator status-operational">
                🔒 Security Level: {}
            </div>
            <div class="status-indicator status-operational">
                📡 Data Feed: {}
            </div>
            <div class="status-indicator status-operational">
                🚨 Alerts: {}
            </div>
            <div class="status-indicator status-operational">
                {} {}
            </div>
        </div>
    </div>
    """.format(
        st.session_state.system_status['api_status'],
        st.session_state.security_level,
        st.session_state.system_status['data_feed'],
        st.session_state.system_status['alerts'],
        fallback_icon,
        fallback_text
    ), unsafe_allow_html=True)
    
    # API Key Management sidebar
    with st.sidebar:
        
        # Session info at the top
        if st.session_state.get('user_authenticated', False):
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
                color: white;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                text-align: center;
            ">
                <div>👤 <strong>{st.session_state.get('current_user', 'User')}</strong></div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem;">
                    Session: {datetime.now().strftime('%H:%M:%S')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔓 Logout", use_container_width=True):
                for key in ['user_authenticated', 'current_user', 'session_start']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("Logged out successfully")
                st.rerun()
        
        display_api_key_management()
        display_system_controls()
    
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Platform selection
        platforms = st.multiselect(
            "Select Platforms",
            ["Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok"],
            default=["Twitter", "Facebook", "Instagram"]
        )
        
        # Time range selection
        time_range = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            index=2
        )
        
        # Keywords monitoring
        st.subheader("🔍 Keywords")
        keywords = st.text_area(
            "Monitor Keywords (one per line)",
            value="brand name\nproduct launch\ncustomer service"
        ).split('\n')
        
        # Alert thresholds
        st.subheader("🚨 Alert Thresholds")
        mention_threshold = st.slider("Mention Spike Alert", 10, 1000, 100)
        sentiment_threshold = st.slider("Negative Sentiment Alert (%)", 10, 90, 30)
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto Refresh (30s)", value=True)
        
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    # Generate sample data
    df = generate_sample_data(platforms, keywords, time_range)
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Mentions",
            value=f"{metrics['total_mentions']:,}",
            delta=f"{metrics['mentions_change']:+.1%}"
        )
    
    with col2:
        st.metric(
            label="Avg Sentiment",
            value=f"{metrics['avg_sentiment']:.2f}",
            delta=f"{metrics['sentiment_change']:+.2f}"
        )
    
    with col3:
        st.metric(
            label="Engagement Rate",
            value=f"{metrics['engagement_rate']:.1%}",
            delta=f"{metrics['engagement_change']:+.1%}"
        )
    
    with col4:
        st.metric(
            label="Reach",
            value=f"{metrics['total_reach']:,.0f}",
            delta=f"{metrics['reach_change']:+.1%}"
        )
    
    # Alert system
    alerts = check_alerts(df, mention_threshold, sentiment_threshold)
    if alerts:
        st.subheader("🚨 Active Alerts")
        display_alerts(alerts)
    
    # Main dashboard content
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Analytics", "🌍 Geographic", "📝 Content"])
    
    with tab1:
        # Mentions over time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Mentions Over Time")
            mentions_chart = create_mentions_chart(df)
            st.plotly_chart(mentions_chart, use_container_width=True)
        
        with col2:
            st.subheader("Sentiment Distribution")
            sentiment_chart = create_sentiment_chart(df)
            st.plotly_chart(sentiment_chart, use_container_width=True)
        
        # Platform breakdown
        st.subheader("Platform Performance")
        platform_chart = create_platform_chart(df)
        st.plotly_chart(platform_chart, use_container_width=True)
    
    with tab2:
        # Detailed analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Engagement by Platform")
            engagement_chart = create_engagement_chart(df)
            st.plotly_chart(engagement_chart, use_container_width=True)
        
        with col2:
            st.subheader("Top Keywords")
            keyword_chart = create_keyword_chart(df, keywords)
            st.plotly_chart(keyword_chart, use_container_width=True)
        
        # Correlation matrix
        st.subheader("Metrics Correlation")
        correlation_chart = create_correlation_chart(df)
        st.plotly_chart(correlation_chart, use_container_width=True)
    
    with tab3:
        # Geographic analysis
        st.subheader("Geographic Distribution")
        geo_chart = create_geographic_chart(df)
        st.plotly_chart(geo_chart, use_container_width=True)
        
        # Top locations table
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Countries")
            country_data = df.groupby('country').agg({
                'mentions': 'sum',
                'sentiment': 'mean'
            }).round(2).sort_values('mentions', ascending=False).head(10)
            st.dataframe(country_data)
        
        with col2:
            st.subheader("Top Cities")
            city_data = df.groupby('city').agg({
                'mentions': 'sum',
                'engagement': 'mean'
            }).round(2).sort_values('mentions', ascending=False).head(10)
            st.dataframe(city_data)
    
    with tab4:
        # Content analysis
        st.subheader("Top Performing Content")
        top_content = df.nlargest(10, 'engagement')[['content', 'platform', 'engagement', 'sentiment', 'timestamp']]
        st.dataframe(top_content, use_container_width=True)
        
        # Word cloud placeholder
        st.subheader("Trending Topics")
        st.info("Word cloud visualization would be implemented here with libraries like wordcloud")

def create_mentions_chart(df):
    """Create mentions over time chart"""
    mentions_by_time = df.groupby(['timestamp', 'platform'])['mentions'].sum().reset_index()
    
    fig = px.line(
        mentions_by_time, 
        x='timestamp', 
        y='mentions', 
        color='platform',
        title="Mentions Over Time by Platform"
    )
    fig.update_layout(height=400)
    return fig

def create_sentiment_chart(df):
    """Create sentiment distribution chart"""
    sentiment_dist = df['sentiment_category'].value_counts()
    
    fig = px.pie(
        values=sentiment_dist.values,
        names=sentiment_dist.index,
        title="Sentiment Distribution",
        color_discrete_map={
            'Positive': '#4CAF50',
            'Negative': '#F44336',
            'Neutral': '#FF9800'
        }
    )
    fig.update_layout(height=400)
    return fig

def create_platform_chart(df):
    """Create platform performance chart"""
    platform_metrics = df.groupby('platform').agg({
        'mentions': 'sum',
        'engagement': 'mean',
        'sentiment': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Mentions', 'Avg Engagement', 'Avg Sentiment'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['mentions'], name='Mentions'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['engagement'], name='Engagement'),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['sentiment'], name='Sentiment'),
        row=1, col=3
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def create_engagement_chart(df):
    """Create engagement analysis chart"""
    engagement_by_platform = df.groupby(['platform', 'sentiment_category'])['engagement'].mean().reset_index()
    
    fig = px.bar(
        engagement_by_platform,
        x='platform',
        y='engagement',
        color='sentiment_category',
        title="Average Engagement by Platform and Sentiment",
        color_discrete_map={
            'Positive': '#4CAF50',
            'Negative': '#F44336',
            'Neutral': '#FF9800'
        }
    )
    fig.update_layout(height=400)
    return fig

def create_keyword_chart(df, keywords):
    """Create keyword performance chart"""
    # Simulate keyword data
    keyword_data = []
    for keyword in keywords[:5]:  # Top 5 keywords
        keyword_mentions = np.random.randint(10, 200)
        keyword_data.append({
            'keyword': keyword,
            'mentions': keyword_mentions,
            'sentiment': np.random.uniform(-1, 1)
        })
    
    keyword_df = pd.DataFrame(keyword_data)
    
    fig = px.scatter(
        keyword_df,
        x='mentions',
        y='sentiment',
        size='mentions',
        hover_name='keyword',
        title="Keyword Performance (Mentions vs Sentiment)"
    )
    fig.update_layout(height=400)
    return fig

def create_correlation_chart(df):
    """Create correlation matrix chart"""
    corr_data = df[['mentions', 'engagement', 'sentiment', 'reach']].corr()
    
    fig = px.imshow(
        corr_data,
        title="Metrics Correlation Matrix",
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig.update_layout(height=400)
    return fig

def create_geographic_chart(df):
    """Create geographic distribution chart"""
    geo_data = df.groupby('country')['mentions'].sum().reset_index()
    
    fig = px.choropleth(
        geo_data,
        locations='country',
        color='mentions',
        locationmode='country names',
        title="Global Mention Distribution",
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=500)
    return fig

def display_api_key_management():
    """Display API key management interface"""
    st.header("🔐 Security Center")
    
    # Link to dedicated API Management page
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
    ">
        <h4>🔑 ADVANCED API MANAGEMENT</h4>
        <p>For comprehensive API configuration, testing, and monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open API Management Center", type="primary", use_container_width=True):
        st.info("Navigate to the '🔑 API Management' page in the sidebar for full API configuration")
    
    # New Intelligence Operations link
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
    ">
        <h4>🎯 INTELLIGENCE OPERATIONS</h4>
        <p>Advanced multi-platform monitoring and threat analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Intelligence Ops", type="primary", use_container_width=True):
        st.info("Navigate to the '🎯 Intelligence Operations' page for advanced monitoring capabilities")
    
    # New NLP Analysis Engine link
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    ">
        <h4>🧠 NLP ANALYSIS ENGINE</h4>
        <p>AI-powered content analysis with threat detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch NLP Engine", type="primary", use_container_width=True):
        st.info("Navigate to the '🧠 NLP Analysis' page for advanced AI-powered content analysis")    # Quick API Status Overview
    with st.expander("📊 Quick API Status", expanded=True):
        st.markdown("""
        <div class="sidebar-info">
            <strong>⚠️ Security Notice:</strong><br>
            API keys are stored in session memory only for security.
        </div>
        """, unsafe_allow_html=True)
        
        # Show current API connection status
        connected_count = sum(1 for api in st.session_state.api_keys.values() if api['status'] == 'connected')
        total_apis = len(st.session_state.api_keys)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Connected APIs", f"{connected_count}/{total_apis}")
        with col2:
            percentage = (connected_count/total_apis)*100 if total_apis > 0 else 0
            st.metric("Status", f"{percentage:.0f}% Ready")
        
        # API Status indicators
        for api_name, api_data in st.session_state.api_keys.items():
            status = api_data['status']
            is_demo = api_data.get('is_demo', False)
            
            if status == 'connected':
                if is_demo:
                    st.markdown(f"🎯 {api_name.title().replace('_', ' ')}: Demo Mode")
                else:
                    st.markdown(f"🟢 {api_name.title().replace('_', ' ')}: Connected")
            elif status == 'testing':
                st.markdown(f"🟡 {api_name.title().replace('_', ' ')}: Testing...")
            elif status == 'error':
                st.markdown(f"🔴 {api_name.title().replace('_', ' ')}: Error")
            else:
                st.markdown(f"⚪ {api_name.title().replace('_', ' ')}: Not configured")
        
        # Quick setup reminder
        if connected_count == 0:
            st.warning("⚠️ No APIs configured. Visit API Management page to set up connections.")

def display_system_controls():
    """Display system control panel"""
    st.header("⚙️ System Controls")
    
    # Security Level
    with st.expander("🔒 Security Settings", expanded=False):
        security_level = st.selectbox(
            "Security Level",
            ["LOW", "MEDIUM", "HIGH", "MAXIMUM"],
            index=2,
            help="Higher levels enable additional security measures"
        )
        st.session_state.security_level = security_level
        
        # Encryption settings
        st.checkbox("🔐 Enable End-to-End Encryption", value=True)
        st.checkbox("🛡️ Enable Two-Factor Authentication", value=True)
        st.checkbox("📝 Enable Audit Logging", value=True)
        
        if st.button("🔄 Refresh Security Status"):
            st.session_state.system_status['security'] = 'SECURE'
            st.success("Security status refreshed")
    
    # System Monitoring
    with st.expander("📊 System Health", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU Usage
            cpu_usage = np.random.uniform(15, 85)
            st.metric(
                "CPU Usage", 
                f"{cpu_usage:.1f}%",
                delta=f"{np.random.uniform(-5, 5):+.1f}%"
            )
            
            # Memory Usage
            memory_usage = np.random.uniform(40, 80)
            st.metric(
                "Memory", 
                f"{memory_usage:.1f}%",
                delta=f"{np.random.uniform(-3, 3):+.1f}%"
            )
        
        with col2:
            # Network Status
            network_latency = np.random.uniform(10, 50)
            st.metric(
                "Network Latency", 
                f"{network_latency:.0f}ms",
                delta=f"{np.random.uniform(-5, 5):+.0f}ms"
            )
            
            # Active Connections
            connections = np.random.randint(50, 200)
            st.metric(
                "Connections", 
                f"{connections}",
                delta=f"{np.random.randint(-10, 10):+d}"
            )
        
        # System health indicator
        if cpu_usage < 70 and memory_usage < 70:
            st.markdown('<div class="health-indicator health-good">🟢 System Healthy</div>', unsafe_allow_html=True)
        elif cpu_usage < 85 and memory_usage < 85:
            st.markdown('<div class="health-indicator health-warning">🟡 System Load High</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="health-indicator health-critical">🔴 System Critical</div>', unsafe_allow_html=True)
    
    # Emergency Controls
    with st.expander("🚨 Emergency Controls", expanded=False):
        st.markdown("""
        <div class="sidebar-info" style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);">
            <strong>⚠️ Emergency Operations</strong><br>
            Use only in critical situations
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔴 Emergency Stop", type="secondary"):
                st.error("Emergency stop activated!")
        
        with col2:
            if st.button("🔄 System Reset", type="secondary"):
                st.warning("System reset initiated...")

def check_api_status():
    """Check status of all APIs"""
    import random
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']
    statuses = ['ACTIVE', 'LIMITED', 'INACTIVE']
    
    return {platform: random.choice(statuses) for platform in platforms}

if __name__ == "__main__":
    main()
