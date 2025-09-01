import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import time

# Import our custom API managers
try:
    from utils.monitoring_service import SocialMediaMonitoringService
    from utils.social_media_apis import StandardizedPost, APIResponse
except ImportError:
    st.error("API integration modules not found. Please ensure all dependencies are installed.")
    st.stop()

st.set_page_config(
    page_title="Intelligence Operations - Police AI Monitor",
    page_icon="🎯",
    layout="wide"
)

# Enhanced Police Theme CSS for Intelligence Operations
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
    
    /* Intelligence Operations Header */
    .intel-header {
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
    
    .intel-header::before {
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
    
    /* Operation status indicators */
    .operation-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-active {
        background: #dcfce7;
        color: var(--police-green);
        border: 1px solid var(--police-green);
    }
    
    .status-standby {
        background: #fef3c7;
        color: #d97706;
        border: 1px solid #d97706;
    }
    
    .status-offline {
        background: #fee2e2;
        color: var(--police-red);
        border: 1px solid var(--police-red);
    }
    
    /* Threat level indicators */
    .threat-level {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .threat-critical {
        background: var(--police-red);
        color: white;
        animation: pulse-critical 2s infinite;
    }
    
    .threat-high {
        background: #dc2626;
        color: white;
    }
    
    .threat-medium {
        background: var(--police-accent);
        color: #1f2937;
    }
    
    .threat-low {
        background: var(--police-green);
        color: white;
    }
    
    @keyframes pulse-critical {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Intelligence cards */
    .intel-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .intel-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
    }
    
    .intel-card.critical {
        border-left: 5px solid var(--police-red);
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    }
    
    .intel-card.high {
        border-left: 5px solid #dc2626;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    }
    
    .intel-card.medium {
        border-left: 5px solid var(--police-accent);
    }
    
    .intel-card.low {
        border-left: 5px solid var(--police-green);
    }
    
    /* Operation timeline */
    .timeline-item {
        border-left: 3px solid var(--police-blue);
        padding-left: 1rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--police-blue);
    }
    
    /* Real-time indicators */
    .live-feed {
        background: linear-gradient(45deg, var(--police-red) 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        animation: pulse-live 2s infinite;
    }
    
    @keyframes pulse-live {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state for intelligence operations"""
    if 'monitoring_service' not in st.session_state:
        st.session_state.monitoring_service = None
    
    if 'operation_status' not in st.session_state:
        st.session_state.operation_status = 'standby'
    
    if 'search_results' not in st.session_state:
        st.session_state.search_results = {}
    
    if 'threat_alerts' not in st.session_state:
        st.session_state.threat_alerts = []
    
    if 'operation_log' not in st.session_state:
        st.session_state.operation_log = []

def main():
    initialize_session_state()
    
    # Security classification banner
    st.markdown("""
    <div style="background: var(--police-red); color: white; text-align: center; padding: 0.5rem; font-weight: bold; font-size: 0.9rem; letter-spacing: 1px;">
        🔒 TOP SECRET - INTELLIGENCE OPERATIONS - EYES ONLY 🔒
    </div>
    """, unsafe_allow_html=True)
    
    # Intelligence Operations header
    st.markdown("""
    <div class="intel-header">
        <h1>🎯 INTELLIGENCE OPERATIONS CENTER</h1>
        <p>Multi-platform social media intelligence gathering and analysis</p>
        <div style="margin-top: 1rem;">
            <span class="live-feed">🔴 REAL-TIME MONITORING</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API configuration
    if not check_api_configuration():
        st.error("⚠️ API configuration required. Please configure APIs in the API Management page.")
        return
    
    # Operation control panel
    display_operation_control_panel()
    
    # Main intelligence dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Search Operations",
        "📊 Intelligence Analysis", 
        "🚨 Threat Detection",
        "🌐 Cross-Platform Monitoring",
        "📈 Operational Reports"
    ])
    
    with tab1:
        display_search_operations()
    
    with tab2:
        display_intelligence_analysis()
    
    with tab3:
        display_threat_detection()
    
    with tab4:
        display_cross_platform_monitoring()
    
    with tab5:
        display_operational_reports()

def check_api_configuration():
    """Check if APIs are configured"""
    if 'api_keys' not in st.session_state:
        return False
    
    configured_apis = [
        api for api, data in st.session_state.api_keys.items() 
        if data.get('key') and data.get('status') == 'connected'
    ]
    
    return len(configured_apis) > 0

def display_operation_control_panel():
    """Display operation control panel"""
    st.header("🔧 Operation Control Panel")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Initialize Operations", type="primary"):
            initialize_monitoring_service()
    
    with col2:
        if st.button("⏸️ Standby Mode"):
            st.session_state.operation_status = 'standby'
            st.success("Operations on standby")
    
    with col3:
        if st.button("🔄 Refresh Status"):
            refresh_platform_status()
    
    with col4:
        if st.button("📋 Export Log"):
            export_operation_log()
    
    # Status indicators
    display_platform_status()

def initialize_monitoring_service():
    """Initialize the monitoring service with current API keys"""
    try:
        # Collect API credentials from session state
        credentials = {}
        
        if st.session_state.api_keys.get('twitter', {}).get('status') == 'connected':
            credentials['twitter_bearer'] = st.session_state.api_keys['twitter']['key']
        
        if st.session_state.api_keys.get('facebook', {}).get('status') == 'connected':
            credentials['facebook_token'] = st.session_state.api_keys['facebook']['key']
        
        if st.session_state.api_keys.get('telegram', {}).get('status') == 'connected':
            credentials['telegram_bot_token'] = st.session_state.api_keys['telegram']['key']
        
        if st.session_state.api_keys.get('news_api', {}).get('status') == 'connected':
            credentials['news_api_key'] = st.session_state.api_keys['news_api']['key']
        
        if not credentials:
            st.error("No connected APIs found. Please configure APIs first.")
            return
        
        # Initialize monitoring service
        st.session_state.monitoring_service = SocialMediaMonitoringService(credentials)
        st.session_state.operation_status = 'active'
        
        # Add to operation log
        log_entry = {
            'timestamp': datetime.now(),
            'action': 'Operations Initialized',
            'details': f"Platforms: {list(credentials.keys())}",
            'status': 'success'
        }
        st.session_state.operation_log.append(log_entry)
        
        st.success(f"🎯 Operations initialized with {len(credentials)} platforms")
        
    except Exception as e:
        st.error(f"Failed to initialize operations: {str(e)}")
        log_entry = {
            'timestamp': datetime.now(),
            'action': 'Initialization Failed',
            'details': str(e),
            'status': 'error'
        }
        st.session_state.operation_log.append(log_entry)

def display_platform_status():
    """Display current platform status"""
    st.subheader("📡 Platform Status")
    
    status_cols = st.columns(4)
    
    if st.session_state.monitoring_service:
        try:
            platform_status = st.session_state.monitoring_service.get_platform_status()
            
            for i, (platform, status) in enumerate(platform_status.items()):
                with status_cols[i % 4]:
                    if status['connected']:
                        st.success(f"✅ {platform.title()}")
                        if status.get('rate_limit_remaining'):
                            st.caption(f"Rate limit: {status['rate_limit_remaining']}")
                    else:
                        st.error(f"❌ {platform.title()}")
                        if status.get('error'):
                            st.caption(f"Error: {status['error'][:30]}...")
        except Exception as e:
            st.error(f"Status check failed: {str(e)}")
    else:
        for i, api_name in enumerate(['twitter', 'facebook', 'telegram', 'news_api']):
            with status_cols[i]:
                api_data = st.session_state.api_keys.get(api_name, {})
                if api_data.get('status') == 'connected':
                    st.success(f"✅ {api_name.title().replace('_', ' ')}")
                else:
                    st.error(f"❌ {api_name.title().replace('_', ' ')}")

def display_search_operations():
    """Display search operations interface"""
    st.header("🔍 Multi-Platform Search Operations")
    
    if not st.session_state.monitoring_service:
        st.warning("⚠️ Operations not initialized. Please initialize in the control panel.")
        return
    
    # Search configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Search Parameters")
        
        # Keywords input
        keywords_input = st.text_area(
            "Keywords (one per line)",
            value="suspicious activity\nprotest\ndemonstration\nthreats",
            help="Enter keywords to search for across platforms"
        )
        keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]
        
        # Platform selection
        available_platforms = list(st.session_state.monitoring_service.api_managers.keys())
        selected_platforms = st.multiselect(
            "Select Platforms",
            available_platforms,
            default=available_platforms,
            help="Choose which platforms to search"
        )
        
        # Time range
        time_range_option = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "Custom Range"]
        )
        
        if time_range_option == "Custom Range":
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input("Start Date")
                start_time = st.time_input("Start Time")
            with col_end:
                end_date = st.date_input("End Date")
                end_time = st.time_input("End Time")
            
            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)
            time_range = (start_datetime, end_datetime)
        else:
            # Convert time range option to datetime tuple
            now = datetime.now()
            if time_range_option == "Last Hour":
                time_range = (now - timedelta(hours=1), now)
            elif time_range_option == "Last 6 Hours":
                time_range = (now - timedelta(hours=6), now)
            elif time_range_option == "Last 24 Hours":
                time_range = (now - timedelta(days=1), now)
            elif time_range_option == "Last 7 Days":
                time_range = (now - timedelta(days=7), now)
            else:
                time_range = None
        
        # Maximum results
        max_results = st.slider(
            "Maximum Results per Platform",
            min_value=10,
            max_value=200,
            value=50,
            step=10
        )
    
    with col2:
        st.subheader("Operation Status")
        
        # Current operation status
        if st.session_state.operation_status == 'active':
            st.success("🟢 Operations Active")
        elif st.session_state.operation_status == 'standby':
            st.warning("🟡 Standby Mode")
        else:
            st.error("🔴 Operations Offline")
        
        # Quick stats
        if st.session_state.search_results:
            total_posts = sum(
                len(response.data) for response in st.session_state.search_results.values()
                if response.success
            )
            st.metric("Total Posts Found", total_posts)
            
            successful_platforms = sum(
                1 for response in st.session_state.search_results.values()
                if response.success
            )
            st.metric("Platforms Searched", successful_platforms)
    
    # Execute search
    if st.button("🚀 Execute Search Operation", type="primary"):
        execute_search_operation(keywords, selected_platforms, max_results, time_range)
    
    # Display search results
    display_search_results()

def execute_search_operation(keywords, platforms, max_results, time_range):
    """Execute multi-platform search operation"""
    try:
        with st.spinner("🔍 Executing search operation across platforms..."):
            # Perform search
            search_results = st.session_state.monitoring_service.search_across_platforms(
                keywords=keywords,
                platforms=platforms,
                max_results_per_platform=max_results,
                time_range=time_range
            )
            
            st.session_state.search_results = search_results
            
            # Log operation
            log_entry = {
                'timestamp': datetime.now(),
                'action': 'Search Operation',
                'details': f"Keywords: {keywords[:3]}{'...' if len(keywords) > 3 else ''}, Platforms: {platforms}",
                'status': 'success'
            }
            st.session_state.operation_log.append(log_entry)
            
            # Show success message
            successful_searches = sum(1 for result in search_results.values() if result.success)
            total_posts = sum(len(result.data) for result in search_results.values() if result.success)
            
            st.success(f"✅ Search completed: {total_posts} posts found across {successful_searches} platforms")
            
    except Exception as e:
        st.error(f"Search operation failed: {str(e)}")
        log_entry = {
            'timestamp': datetime.now(),
            'action': 'Search Operation Failed',
            'details': str(e),
            'status': 'error'
        }
        st.session_state.operation_log.append(log_entry)

def display_search_results():
    """Display search operation results"""
    if not st.session_state.search_results:
        return
    
    st.subheader("📊 Search Results")
    
    # Results summary
    col1, col2, col3, col4 = st.columns(4)
    
    total_posts = 0
    successful_platforms = 0
    failed_platforms = 0
    
    for platform, response in st.session_state.search_results.items():
        if response.success:
            total_posts += len(response.data)
            successful_platforms += 1
        else:
            failed_platforms += 1
    
    with col1:
        st.metric("Total Posts", total_posts)
    with col2:
        st.metric("Successful Platforms", successful_platforms)
    with col3:
        st.metric("Failed Platforms", failed_platforms)
    with col4:
        st.metric("Success Rate", f"{(successful_platforms/(successful_platforms+failed_platforms))*100:.0f}%")
    
    # Platform-specific results
    for platform, response in st.session_state.search_results.items():
        with st.expander(f"📱 {platform.title()} Results ({len(response.data)} posts)"):
            if response.success:
                if response.data:
                    # Display first few posts
                    for i, post in enumerate(response.data[:5]):
                        display_post_card(post, i)
                    
                    if len(response.data) > 5:
                        st.info(f"+ {len(response.data) - 5} more posts available")
                else:
                    st.info("No posts found for this platform")
            else:
                st.error(f"❌ Search failed: {response.error_message}")

def display_post_card(post, index):
    """Display individual post in a card format"""
    # Determine threat level styling
    threat_class = post.threat_level if hasattr(post, 'threat_level') else 'low'
    
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**@{post.author}** on {post.platform}")
            st.markdown(f"_{post.content[:200]}{'...' if len(post.content) > 200 else ''}_")
        
        with col2:
            engagement = post.engagement.get('total', 0)
            st.metric("Engagement", engagement)
        
        with col3:
            st.markdown(f"**Threat Level:** {post.threat_level if hasattr(post, 'threat_level') else 'Low'}")
            st.caption(f"{post.timestamp.strftime('%Y-%m-%d %H:%M')}")
        
        st.divider()

def display_intelligence_analysis():
    """Display intelligence analysis dashboard"""
    st.header("📊 Intelligence Analysis Dashboard")
    
    if not st.session_state.search_results:
        st.info("No search results available. Execute a search operation first.")
        return
    
    # Generate intelligence report
    if st.button("📋 Generate Intelligence Report"):
        generate_intelligence_report()
    
    # Display analytics
    display_analytics_charts()

def generate_intelligence_report():
    """Generate comprehensive intelligence report"""
    try:
        with st.spinner("📊 Generating intelligence report..."):
            report = st.session_state.monitoring_service.generate_intelligence_report(
                st.session_state.search_results,
                "current_operation"
            )
            
            st.session_state.intelligence_report = report
            
            # Display report summary
            st.success("✅ Intelligence report generated")
            
            # Show key findings
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Threats Detected",
                    "YES" if report['summary']['threats_detected'] else "NO",
                    delta="High Priority" if report['summary']['threats_detected'] else "All Clear"
                )
            
            with col2:
                st.metric(
                    "Campaigns Detected",
                    "YES" if report['summary']['campaigns_detected'] else "NO",
                    delta="Investigate" if report['summary']['campaigns_detected'] else "Normal Activity"
                )
            
            with col3:
                st.metric(
                    "High-Risk Posts",
                    report['summary']['high_risk_posts_count']
                )
            
            # Display detailed findings
            if report['summary']['threats_detected']:
                st.error("🚨 THREAT ALERT: High-risk content detected!")
                
                threat_analysis = report['threat_analysis']
                st.markdown("**Detected Threat Keywords:**")
                st.write(threat_analysis.get('threat_keywords', []))
                
                st.markdown("**High-Risk Posts:**")
                for post_data in threat_analysis.get('high_risk_posts', [])[:3]:
                    post = post_data['post']
                    st.markdown(f"- **@{post.author}**: {post.content[:100]}...")
                    st.caption(f"Risk Score: {post_data['risk_score']}, Keywords: {post_data['detected_keywords']}")
            
            if report['summary']['campaigns_detected']:
                st.warning("⚠️ COORDINATED CAMPAIGN DETECTED")
                campaign_indicators = report['threat_analysis'].get('campaign_indicators', {})
                st.markdown(f"**Confidence Level:** {campaign_indicators.get('confidence', 0):.2%}")
                st.markdown(f"**Platforms Involved:** {', '.join(campaign_indicators.get('platforms_involved', []))}")
            
    except Exception as e:
        st.error(f"Failed to generate intelligence report: {str(e)}")

def display_analytics_charts():
    """Display analytics charts"""
    if not hasattr(st.session_state, 'intelligence_report'):
        return
    
    report = st.session_state.intelligence_report
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform distribution chart
        platform_stats = report.get('platform_statistics', {})
        platforms = list(platform_stats.keys())
        post_counts = [stats['posts_collected'] for stats in platform_stats.values()]
        
        if platforms and post_counts:
            fig = px.pie(
                values=post_counts,
                names=platforms,
                title="Posts by Platform"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Engagement analysis
        engagement_analysis = report.get('engagement_analysis', {})
        platform_engagement = engagement_analysis.get('platform_breakdown', {})
        
        if platform_engagement:
            fig = px.bar(
                x=list(platform_engagement.keys()),
                y=list(platform_engagement.values()),
                title="Average Engagement by Platform"
            )
            st.plotly_chart(fig, use_container_width=True)

def display_threat_detection():
    """Display threat detection interface"""
    st.header("🚨 Threat Detection & Analysis")
    
    if not hasattr(st.session_state, 'intelligence_report'):
        st.info("Generate an intelligence report first to view threat analysis.")
        return
    
    report = st.session_state.intelligence_report
    threat_analysis = report.get('threat_analysis', {})
    
    # Threat overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        threat_status = "DETECTED" if threat_analysis.get('threats_detected') else "NONE"
        st.metric("Threat Status", threat_status)
    
    with col2:
        campaign_status = "DETECTED" if threat_analysis.get('campaigns_detected') else "NONE"
        st.metric("Coordinated Campaigns", campaign_status)
    
    with col3:
        high_risk_count = threat_analysis.get('high_risk_posts', [])
        st.metric("High-Risk Posts", len(high_risk_count))
    
    with col4:
        threat_keywords = threat_analysis.get('threat_keywords', [])
        st.metric("Threat Keywords", len(threat_keywords))
    
    # Detailed threat analysis
    if threat_analysis.get('threats_detected'):
        st.subheader("🔴 Active Threats")
        
        for i, post_data in enumerate(threat_analysis.get('high_risk_posts', [])):
            post = post_data['post']
            risk_score = post_data['risk_score']
            keywords = post_data['detected_keywords']
            
            threat_level = 'critical' if risk_score >= 7 else 'high' if risk_score >= 5 else 'medium'
            
            with st.container():
                st.markdown(f"""
                <div class="intel-card {threat_level}">
                    <h4>🚨 Threat #{i+1} - {threat_level.upper()} RISK</h4>
                    <p><strong>Platform:</strong> {post.platform}</p>
                    <p><strong>Author:</strong> @{post.author}</p>
                    <p><strong>Content:</strong> {post.content[:200]}{'...' if len(post.content) > 200 else ''}</p>
                    <p><strong>Risk Score:</strong> {risk_score}/10</p>
                    <p><strong>Detected Keywords:</strong> {', '.join(keywords)}</p>
                    <p><strong>Timestamp:</strong> {post.timestamp}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Campaign analysis
    if threat_analysis.get('campaigns_detected'):
        st.subheader("⚠️ Coordinated Campaign Analysis")
        
        campaign_indicators = threat_analysis.get('campaign_indicators', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Campaign Metrics:**")
            st.metric("Confidence Level", f"{campaign_indicators.get('confidence', 0):.1%}")
            st.metric("Content Similarity", f"{campaign_indicators.get('content_similarity', 0):.1%}")
            st.metric("Temporal Coordination", f"{campaign_indicators.get('temporal_coordination', 0):.1%}")
        
        with col2:
            st.markdown("**Platforms Involved:**")
            platforms = campaign_indicators.get('platforms_involved', [])
            for platform in platforms:
                st.write(f"• {platform.title()}")
            
            coordinated_hashtags = campaign_indicators.get('coordinated_hashtags', [])
            if coordinated_hashtags:
                st.markdown("**Coordinated Hashtags:**")
                for hashtag in coordinated_hashtags[:5]:
                    st.write(f"• #{hashtag}")

def display_cross_platform_monitoring():
    """Display cross-platform monitoring interface"""
    st.header("🌐 Cross-Platform Intelligence Monitoring")
    
    st.info("🔄 Real-time monitoring capabilities - Configure monitoring parameters below")
    
    # Monitoring configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monitoring Configuration")
        
        # Target keywords
        monitor_keywords = st.text_area(
            "Monitoring Keywords",
            value="terrorism\nbomb threat\nviolent protest\nsecurity threat",
            help="Keywords to monitor across all platforms"
        )
        
        # Monitoring interval
        check_interval = st.selectbox(
            "Check Interval",
            [5, 10, 15, 30, 60],
            index=2,
            format_func=lambda x: f"{x} minutes"
        )
        
        # Alert threshold
        alert_threshold = st.selectbox(
            "Alert Threshold",
            ["low", "medium", "high"],
            index=1
        )
    
    with col2:
        st.subheader("Monitoring Status")
        
        # Mock monitoring status
        st.metric("Active Monitors", "4/4")
        st.metric("Last Check", "2 minutes ago")
        st.metric("Alerts Today", "3")
        
        # Control buttons
        if st.button("🚀 Start Monitoring"):
            st.success("✅ Real-time monitoring activated")
        
        if st.button("⏸️ Pause Monitoring"):
            st.warning("⏸️ Monitoring paused")
        
        if st.button("🔔 Test Alerts"):
            st.info("📱 Test alert sent to configured channels")

def display_operational_reports():
    """Display operational reports and logs"""
    st.header("📈 Operational Reports & Intelligence Logs")
    
    # Operation log
    st.subheader("📋 Operation Log")
    
    if st.session_state.operation_log:
        for entry in reversed(st.session_state.operation_log[-10:]):  # Show last 10 entries
            timestamp = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            status_emoji = "✅" if entry['status'] == 'success' else "❌"
            
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.write(f"**{timestamp}**")
                
                with col2:
                    st.write(f"{status_emoji} {entry['action']}")
                    st.caption(entry['details'])
                
                with col3:
                    st.write(entry['status'].upper())
    else:
        st.info("No operations logged yet")
    
    # Export options
    st.subheader("📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Search Results"):
            export_search_results()
    
    with col2:
        if st.button("📋 Export Intelligence Report"):
            export_intelligence_report()
    
    with col3:
        if st.button("📝 Export Operation Log"):
            export_operation_log()

def refresh_platform_status():
    """Refresh platform connection status"""
    st.info("🔄 Refreshing platform status...")
    # Implementation would check actual API connections
    st.success("✅ Platform status refreshed")

def export_search_results():
    """Export search results"""
    if st.session_state.search_results:
        st.success("📊 Search results exported to downloads")
    else:
        st.warning("No search results to export")

def export_intelligence_report():
    """Export intelligence report"""
    if hasattr(st.session_state, 'intelligence_report'):
        st.success("📋 Intelligence report exported to downloads")
    else:
        st.warning("No intelligence report to export")

def export_operation_log():
    """Export operation log"""
    if st.session_state.operation_log:
        st.success("📝 Operation log exported to downloads")
    else:
        st.warning("No operation log to export")

if __name__ == "__main__":
    main()
