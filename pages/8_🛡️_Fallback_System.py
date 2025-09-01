#!/usr/bin/env python3
"""
🛡️ FALLBACK SYSTEM INTERFACE
Streamlit interface for police monitoring fallback system
Provides comprehensive offline capabilities and system management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import sys
import os

# Add utils directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

try:
    from fallback_system import PoliceMonitoringFallbackSystem, SystemMode, AlertLevel
except ImportError:
    st.error("Unable to import fallback system. Please ensure all dependencies are installed.")
    st.stop()

def initialize_fallback_system():
    """Initialize fallback system with session state"""
    if 'fallback_system' not in st.session_state:
        try:
            st.session_state.fallback_system = PoliceMonitoringFallbackSystem()
            st.session_state.system_initialized = True
        except Exception as e:
            st.error(f"Error initializing fallback system: {str(e)}")
            st.session_state.system_initialized = False
    
    return st.session_state.get('fallback_system')

def create_system_status_dashboard():
    """Create system status dashboard"""
    st.subheader("🚥 System Status Dashboard")
    
    fallback_system = st.session_state.fallback_system
    status = fallback_system.get_system_status()
    
    # System health metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        health_color = "🟢" if status['system_health'] > 80 else "🟡" if status['system_health'] > 50 else "🔴"
        st.metric("System Health", f"{status['system_health']:.1f}%", help="Overall system availability")
        st.write(f"{health_color} {status['current_mode'].upper()}")
    
    with col2:
        cached_posts = status.get('cached_data', {}).get('posts_available', 0)
        st.metric("Cached Posts", cached_posts, help="Available cached social media posts")
        st.write("📁 Offline Ready")
    
    with col3:
        total_alerts = status.get('alerts', {}).get('total_alerts', 0)
        recent_alerts = status.get('alerts', {}).get('recent_alerts', 0)
        st.metric("System Alerts", total_alerts, delta=recent_alerts, help="Total system alerts")
        st.write("🚨 Alert System")
    
    with col4:
        api_count = len(status.get('api_status', {}))
        online_count = len([api for api, info in status.get('api_status', {}).items() if info['status'] == 'ONLINE'])
        st.metric("APIs Online", f"{online_count}/{api_count}", help="API availability status")
        st.write("🔗 Connectivity")
    
    # API Status Details
    st.subheader("📡 API Status Details")
    api_status_data = []
    for api_name, api_info in status.get('api_status', {}).items():
        api_status_data.append({
            'API': api_name.title(),
            'Status': api_info['status'],
            'Last Check': api_info['last_check'][:19].replace('T', ' ')
        })
    
    if api_status_data:
        df_apis = pd.DataFrame(api_status_data)
        
        # Color code status
        def color_status(val):
            if val == 'ONLINE':
                return 'background-color: #d4edda; color: #155724'
            elif val == 'OFFLINE':
                return 'background-color: #f8d7da; color: #721c24'
            else:
                return 'background-color: #fff3cd; color: #856404'
        
        styled_df = df_apis.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)
    
    # System Capabilities
    st.subheader("⚙️ System Capabilities")
    capabilities = status.get('capabilities', {})
    
    cap_col1, cap_col2, cap_col3 = st.columns(3)
    
    with cap_col1:
        st.write("🔍 **Offline Analysis**")
        st.success("✅ Active" if capabilities.get('offline_analysis') else "❌ Inactive")
        
        st.write("🗂️ **Cached Content**")
        st.success("✅ Available" if capabilities.get('cached_content') else "❌ Unavailable")
    
    with cap_col2:
        st.write("🎭 **Mock Data Generation**")
        st.success("✅ Operational" if capabilities.get('mock_data_generation') else "❌ Disabled")
        
        st.write("🛡️ **Graceful Degradation**")
        st.success("✅ Enabled" if capabilities.get('graceful_degradation') else "❌ Disabled")
    
    with cap_col3:
        st.write("🔄 **Recovery Procedures**")
        st.success("✅ Ready" if capabilities.get('recovery_procedures') else "❌ Not Ready")
        
        st.write("📢 **User Notifications**")
        st.success("✅ Active")

def create_mock_data_generator():
    """Create mock data generation interface"""
    st.subheader("🎭 Mock Data Generator")
    
    fallback_system = st.session_state.fallback_system
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Generation Parameters**")
        
        post_count = st.slider("Number of Posts", 1, 100, 20)
        platform = st.selectbox("Platform", ["mixed", "twitter", "facebook", "instagram", "whatsapp", "telegram"])
        
        if st.button("🎲 Generate Mock Data", type="primary"):
            with st.spinner("Generating mock social media data..."):
                mock_posts = fallback_system.generate_mock_social_media_data(post_count, platform)
                st.session_state.mock_posts = mock_posts
                st.success(f"Generated {len(mock_posts)} mock posts!")
    
    with col2:
        st.write("**Real-time Simulation**")
        
        duration = st.slider("Simulation Duration (minutes)", 1, 120, 30)
        
        if st.button("⚡ Start Real-time Simulation"):
            with st.spinner(f"Simulating {duration} minutes of real-time updates..."):
                simulation = fallback_system.simulate_real_time_updates(duration)
                st.session_state.simulation_data = simulation
                st.success(f"Simulated {simulation.get('total_updates', 0)} updates!")
    
    # Display generated mock posts
    if 'mock_posts' in st.session_state:
        st.subheader("📱 Generated Mock Posts")
        
        # Create dataframe for display
        posts_data = []
        for post in st.session_state.mock_posts:
            posts_data.append({
                'Platform': post.platform.title(),
                'Username': post.username,
                'Content': post.content[:100] + "..." if len(post.content) > 100 else post.content,
                'Sentiment': f"{post.sentiment:.2f}",
                'Threat Score': f"{post.threat_score:.2f}",
                'Location': post.location,
                'Language': post.language.title()
            })
        
        df_posts = pd.DataFrame(posts_data)
        
        # Color code threat scores
        def color_threat_score(val):
            threat_val = float(val)
            if threat_val >= 0.7:
                return 'background-color: #f8d7da; color: #721c24'
            elif threat_val >= 0.4:
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #d4edda; color: #155724'
        
        styled_posts = df_posts.style.applymap(color_threat_score, subset=['Threat Score'])
        st.dataframe(styled_posts, use_container_width=True)
        
        # Threat distribution chart
        threat_scores = [post.threat_score for post in st.session_state.mock_posts]
        
        fig_threat = go.Figure(data=[go.Histogram(x=threat_scores, nbinsx=20, name="Threat Score Distribution")])
        fig_threat.update_layout(
            title="Threat Score Distribution",
            xaxis_title="Threat Score",
            yaxis_title="Number of Posts",
            showlegend=False
        )
        st.plotly_chart(fig_threat, use_container_width=True)

def create_offline_analysis_interface():
    """Create offline analysis interface"""
    st.subheader("🔍 Offline Analysis Engine")
    
    fallback_system = st.session_state.fallback_system
    
    # Analysis input
    st.write("**Text Analysis Input**")
    analysis_text = st.text_area(
        "Enter text for analysis:",
        placeholder="Enter social media content, messages, or any text for offline analysis...",
        height=100
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_type = st.selectbox("Analysis Type", [
            "sentiment",
            "threat_detection",
            "language_detection",
            "entity_extraction",
            "geographic_extraction"
        ])
    
    with col2:
        st.write("")  # Spacing
        st.write("")
        if st.button("🔬 Analyze Text", type="primary", disabled=not analysis_text.strip()):
            if analysis_text.strip():
                with st.spinner("Performing offline analysis..."):
                    result = fallback_system.perform_offline_analysis(analysis_text, analysis_type)
                    st.session_state.analysis_result = result
                    st.success("Analysis completed!")
    
    with col3:
        st.write("")  # Spacing
        st.write("")
        if st.button("🔄 Clear Results"):
            if 'analysis_result' in st.session_state:
                del st.session_state.analysis_result
            st.rerun()
    
    # Display analysis results
    if 'analysis_result' in st.session_state:
        result = st.session_state.analysis_result
        
        st.subheader("📊 Analysis Results")
        
        # Create result display based on analysis type
        if analysis_type == "sentiment":
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sentiment_score = result.get('sentiment_score', 0)
                sentiment_color = "🟢" if sentiment_score > 0.1 else "🔴" if sentiment_score < -0.1 else "🟡"
                st.metric("Sentiment Score", f"{sentiment_score:.3f}")
                st.write(f"{sentiment_color} {result.get('sentiment_label', 'Unknown')}")
            
            with col2:
                confidence = result.get('confidence', 0)
                st.metric("Confidence", f"{confidence:.3f}")
                st.progress(confidence)
            
            with col3:
                st.write("**Indicators Found:**")
                st.write(f"Positive: {result.get('positive_indicators', 0)}")
                st.write(f"Negative: {result.get('negative_indicators', 0)}")
                st.write(f"Threat: {result.get('threat_indicators', 0)}")
        
        elif analysis_type == "threat_detection":
            col1, col2 = st.columns(2)
            
            with col1:
                threat_score = result.get('threat_score', 0)
                threat_level = result.get('threat_level', 'UNKNOWN')
                
                level_color = {
                    'HIGH': '🔴',
                    'MEDIUM': '🟡',
                    'LOW': '🟠',
                    'NONE': '🟢'
                }.get(threat_level, '⚫')
                
                st.metric("Threat Score", f"{threat_score:.3f}")
                st.write(f"{level_color} **{threat_level} THREAT**")
                
                confidence = result.get('confidence', 0)
                st.metric("Confidence", f"{confidence:.3f}")
                st.progress(confidence)
            
            with col2:
                st.write("**Threat Categories Detected:**")
                threat_indicators = result.get('threat_indicators', {})
                
                for category, details in threat_indicators.items():
                    st.write(f"**{category.title()}:**")
                    st.write(f"  Keywords: {', '.join(details.get('keywords_found', []))}")
                    st.write(f"  Severity: {details.get('severity', 0):.2f}")
        
        elif analysis_type == "language_detection":
            col1, col2 = st.columns(2)
            
            with col1:
                language = result.get('language', 'unknown')
                confidence = result.get('confidence', 0)
                
                st.metric("Detected Language", language.title())
                st.metric("Confidence", f"{confidence:.3f}")
                st.progress(confidence)
            
            with col2:
                st.write("**Language Scores:**")
                language_scores = result.get('language_scores', {})
                
                for lang, score in language_scores.items():
                    st.write(f"{lang.title()}: {score:.3f}")
        
        elif analysis_type == "entity_extraction":
            entities = result.get('entities', {})
            
            if entities:
                st.write("**Extracted Entities:**")
                
                for entity_type, entity_data in entities.items():
                    with st.expander(f"{entity_type.replace('_', ' ').title()} ({entity_data.get('count', 0)} found)"):
                        for value in entity_data.get('values', []):
                            st.write(f"• {value}")
            else:
                st.info("No entities detected in the provided text.")
        
        elif analysis_type == "geographic_extraction":
            locations = result.get('locations', {})
            
            if locations:
                st.write("**Geographic Locations Found:**")
                
                for location_type, location_list in locations.items():
                    with st.expander(f"{location_type.replace('_', ' ').title()} ({len(location_list)} found)"):
                        for location in location_list:
                            st.write(f"• {location.title()}")
            else:
                st.info("No geographic locations detected in the provided text.")
        
        # Display raw result data
        with st.expander("🔍 View Raw Analysis Data"):
            st.json(result)

def create_cached_content_interface():
    """Create cached content management interface"""
    st.subheader("🗂️ Cached Content Management")
    
    fallback_system = st.session_state.fallback_system
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Filter Options**")
        
        platform_filter = st.selectbox("Platform", ["all", "twitter", "facebook", "instagram", "whatsapp", "telegram"])
        hours_filter = st.slider("Hours of Content", 1, 168, 24)  # Up to 1 week
        
        if st.button("🔄 Refresh Cached Content"):
            platform = None if platform_filter == "all" else platform_filter
            cached_content = fallback_system.get_cached_content(platform, hours_filter)
            st.session_state.cached_content = cached_content
            st.success(f"Loaded {len(cached_content)} cached items")
    
    with col2:
        st.write("**Cache Statistics**")
        
        if 'cached_content' in st.session_state:
            content = st.session_state.cached_content
            
            if content:
                # Platform distribution
                platform_counts = {}
                for item in content:
                    platform = item.get('platform', 'unknown')
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1
                
                # Create pie chart
                fig_platforms = px.pie(
                    values=list(platform_counts.values()),
                    names=list(platform_counts.keys()),
                    title="Cached Content by Platform"
                )
                st.plotly_chart(fig_platforms, use_container_width=True)
            else:
                st.info("No cached content available for the selected filters.")
    
    # Display cached content
    if 'cached_content' in st.session_state and st.session_state.cached_content:
        st.subheader("📋 Cached Content List")
        
        content = st.session_state.cached_content
        
        # Create display dataframe
        display_data = []
        for item in content[:50]:  # Limit display to 50 items
            display_data.append({
                'Platform': item.get('platform', 'Unknown').title(),
                'Username': item.get('username', 'N/A'),
                'Content': item.get('content', '')[:80] + "..." if len(item.get('content', '')) > 80 else item.get('content', ''),
                'Timestamp': item.get('timestamp', '')[:19].replace('T', ' '),
                'Sentiment': f"{item.get('sentiment', 0):.2f}",
                'Threat Score': f"{item.get('threat_score', 0):.2f}",
                'Location': item.get('location', 'N/A')
            })
        
        df_cached = pd.DataFrame(display_data)
        st.dataframe(df_cached, use_container_width=True)
        
        if len(content) > 50:
            st.info(f"Showing first 50 items out of {len(content)} total cached items.")

def create_demo_mode_interface():
    """Create demo mode interface"""
    st.subheader("🎭 Demo Mode")
    
    fallback_system = st.session_state.fallback_system
    
    st.write("""
    Demo mode provides realistic scenarios for training and demonstration purposes.
    It generates comprehensive simulated data including social media posts, alerts, and system events.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎬 Enter Demo Mode", type="primary"):
            with st.spinner("Initializing demo mode..."):
                demo_result = fallback_system.enter_demo_mode()
                st.session_state.demo_data = demo_result
                st.success("Demo mode activated!")
    
    with col2:
        if st.button("🔄 Exit Demo Mode"):
            if 'demo_data' in st.session_state:
                del st.session_state.demo_data
            fallback_system.current_mode = SystemMode.ONLINE
            st.success("Exited demo mode")
            st.rerun()
    
    # Display demo scenario details
    if 'demo_data' in st.session_state:
        demo_data = st.session_state.demo_data
        scenario = demo_data.get('scenario', {})
        
        st.subheader("🎯 Active Demo Scenario")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Scenario:** {scenario.get('name', 'N/A')}")
            st.write(f"**Description:** {scenario.get('description', 'N/A')}")
            st.write(f"**Duration:** {scenario.get('duration', 'N/A')}")
            st.write(f"**Threat Level:** {scenario.get('threat_level', 'N/A')}")
        
        with col2:
            st.write(f"**Participants:**")
            for participant in scenario.get('participants', []):
                st.write(f"• {participant}")
            st.write(f"**Data Points:** {scenario.get('data_points', 0)}")
        
        # Demo metrics
        st.subheader("📊 Demo Metrics")
        demo_metrics = demo_data.get('demo_metrics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Threats Detected", demo_metrics.get('threats_detected', 0))
        
        with col2:
            st.metric("Alerts Generated", demo_metrics.get('alerts_generated', 0))
        
        with col3:
            st.metric("Evidence Collected", demo_metrics.get('evidence_collected', 0))
        
        with col4:
            st.metric("Agencies Coordinated", demo_metrics.get('agencies_coordinated', 0))
        
        # Demo features
        st.subheader("⚙️ Demo Features Active")
        demo_features = demo_data.get('demo_features', [])
        
        cols = st.columns(3)
        for i, feature in enumerate(demo_features):
            with cols[i % 3]:
                st.write(f"✅ {feature}")

def create_system_management_interface():
    """Create system management interface"""
    st.subheader("⚙️ System Management")
    
    fallback_system = st.session_state.fallback_system
    
    # System mode control
    st.write("**System Mode Control**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_mode = fallback_system.get_system_mode()
        st.write(f"**Current Mode:** {current_mode.value.upper()}")
        
        mode_color = {
            'online': '🟢',
            'offline': '🔴',
            'hybrid': '🟡',
            'demo': '🎭',
            'recovery': '🔄'
        }.get(current_mode.value, '⚫')
        
        st.write(f"{mode_color} System Status")
    
    with col2:
        if st.button("🔍 Check API Status"):
            with st.spinner("Checking API availability..."):
                apis = ['twitter', 'facebook', 'instagram', 'whatsapp', 'telegram']
                api_results = {}
                
                for api in apis:
                    is_available = fallback_system.check_api_availability(api)
                    api_results[api] = is_available
                
                st.session_state.api_check_results = api_results
                st.success("API status check completed!")
    
    with col3:
        if st.button("🚨 Test Graceful Degradation"):
            with st.spinner("Testing system degradation..."):
                degradation_result = fallback_system.handle_graceful_degradation(
                    "social_media_apis",
                    "Simulated API failure for testing"
                )
                st.session_state.degradation_test = degradation_result
                st.success("Degradation test completed!")
    
    # Display API check results
    if 'api_check_results' in st.session_state:
        st.subheader("📡 API Status Check Results")
        
        api_results = st.session_state.api_check_results
        
        cols = st.columns(len(api_results))
        for i, (api, status) in enumerate(api_results.items()):
            with cols[i]:
                status_icon = "🟢" if status else "🔴"
                status_text = "ONLINE" if status else "OFFLINE"
                st.write(f"**{api.title()}**")
                st.write(f"{status_icon} {status_text}")
    
    # Display degradation test results
    if 'degradation_test' in st.session_state:
        st.subheader("🛡️ Graceful Degradation Test Results")
        
        degradation = st.session_state.degradation_test
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Degradation ID:** {degradation.get('degradation_id')}")
            st.write(f"**Failed Component:** {degradation.get('failed_component')}")
            st.write(f"**System Status:** {degradation.get('system_status')}")
            st.write(f"**Recovery Initiated:** {degradation.get('recovery_initiated')}")
        
        with col2:
            recovery_details = degradation.get('recovery_details', {})
            st.write(f"**Recovery ID:** {recovery_details.get('recovery_id')}")
            st.write(f"**Success Rate:** {recovery_details.get('success_rate', 0):.1%}")
            st.write(f"**Overall Status:** {recovery_details.get('overall_status')}")
    
    # User notifications
    st.subheader("📢 User Notifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        notification_message = st.text_input("Notification Message", placeholder="Enter notification message...")
        notification_level = st.selectbox("Alert Level", ["INFO", "WARNING", "ERROR", "CRITICAL"])
    
    with col2:
        st.write("")  # Spacing
        st.write("")
        if st.button("📤 Send Notification", disabled=not notification_message.strip()):
            if notification_message.strip():
                alert_level = getattr(AlertLevel, notification_level)
                notification = fallback_system.create_user_notification(
                    notification_message,
                    alert_level,
                    {'source': 'manual', 'timestamp': datetime.now().isoformat()}
                )
                st.success(f"Notification sent: {notification.get('notification_id')}")

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Police Monitoring Fallback System",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🛡️ Police Monitoring Fallback System")
    st.markdown("Comprehensive offline capabilities and graceful degradation for continuous operations")
    
    # Initialize fallback system
    fallback_system = initialize_fallback_system()
    
    if not st.session_state.get('system_initialized'):
        st.error("Failed to initialize fallback system. Please check system configuration.")
        return
    
    # Sidebar navigation
    st.sidebar.title("🛡️ Fallback System")
    page = st.sidebar.selectbox("Select Function", [
        "🚥 System Status",
        "🎭 Mock Data Generator",
        "🔍 Offline Analysis",
        "🗂️ Cached Content",
        "🎬 Demo Mode",
        "⚙️ System Management"
    ])
    
    # Page routing
    if page == "🚥 System Status":
        create_system_status_dashboard()
    elif page == "🎭 Mock Data Generator":
        create_mock_data_generator()
    elif page == "🔍 Offline Analysis":
        create_offline_analysis_interface()
    elif page == "🗂️ Cached Content":
        create_cached_content_interface()
    elif page == "🎬 Demo Mode":
        create_demo_mode_interface()
    elif page == "⚙️ System Management":
        create_system_management_interface()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("🛡️ **Fallback System Active**")
    st.sidebar.markdown("✅ Offline capabilities enabled")
    st.sidebar.markdown("✅ Graceful degradation ready")
    st.sidebar.markdown("✅ Recovery procedures active")

if __name__ == "__main__":
    main()
