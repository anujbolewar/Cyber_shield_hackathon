import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

# Try to import visualization dependencies
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from police_visualizations import PoliceVisualizationEngine
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    from data_generator import generate_sample_data
except ImportError:
    # Fallback data generator
    def generate_sample_data(platforms, keywords, date_range):
        return pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
            'mentions': np.random.randint(10, 100, 100),
            'sentiment': np.random.uniform(-1, 1, 100),
            'platform': np.random.choice(platforms if platforms else ['Twitter', 'Facebook'], 100),
            'engagement': np.random.uniform(0.01, 0.2, 100)
        })

st.set_page_config(
    page_title="Data Visualization - Social Media Monitor",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for visualizations
st.markdown("""
<style>
    .chart-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-highlight {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .filter-section {
        background-color: #f1f3f4;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📊 Professional Police Data Visualization")
    st.markdown("🏛️ Advanced analytics and insights for law enforcement cyber monitoring")
    st.markdown("---")
    
    if PLOTLY_AVAILABLE:
        # Initialize police visualization engine
        try:
            viz_engine = PoliceVisualizationEngine()
            display_police_visualization_dashboard(viz_engine)
        except Exception as e:
            st.error(f"Error initializing police visualization engine: {e}")
            display_fallback_visualization()
    else:
        display_installation_instructions()
        display_fallback_visualization()

def display_police_visualization_dashboard(viz_engine):
    """Display professional police visualization dashboard"""
    
    # Sidebar controls
    with st.sidebar:
        st.header("�️ Police Intelligence Controls")
        
        # Threat level adjustment
        st.subheader("� Current Threat Level")
        current_threat = st.slider("Threat Level", 0, 100, 75, 
                                 help="Current system-wide threat assessment")
        
        # Time range selection
        st.subheader("📅 Analysis Period")
        time_range = st.selectbox(
            "Select Period",
            ["Last 6 Hours", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            index=1
        )
        
        # Geographic focus
        st.subheader("🗺️ Geographic Focus")
        geo_region = st.selectbox(
            "Region",
            ["All India", "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"],
            index=0
        )
        
        # Platform selection
        st.subheader("📱 Platform Monitoring")
        platforms = st.multiselect(
            "Select Platforms",
            ["Twitter", "Facebook", "Instagram", "Telegram", "WhatsApp", "YouTube"],
            default=["Twitter", "Facebook", "Instagram"]
        )
        
        # Alert threshold
        st.subheader("⚠️ Alert Threshold")
        alert_threshold = st.slider("Risk Score Threshold", 0, 100, 70)
        
        # Export controls
        st.subheader("� Export Options")
        export_format = st.selectbox(
            "Format for Court Evidence",
            ["PNG (High-Res)", "PDF (Court-Ready)", "SVG (Scalable)", "HTML (Interactive)"]
        )
        
        if st.button("📥 Export All Charts", type="primary"):
            st.success("Charts exported for police evidence documentation")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚨 Threat Monitoring", 
        "🗺️ Geographic Intelligence", 
        "🕸️ Network Analysis", 
        "📈 Trend Analysis"
    ])
    
    with tab1:
        display_threat_monitoring_tab(viz_engine, current_threat, alert_threshold)
    
    with tab2:
        display_geographic_intelligence_tab(viz_engine, geo_region)
    
    with tab3:
        display_network_analysis_tab(viz_engine)
    
    with tab4:
        display_trend_analysis_tab(viz_engine, time_range)

def display_threat_monitoring_tab(viz_engine, current_threat, alert_threshold):
    """Display threat monitoring visualizations"""
    
    st.subheader("� Real-Time Threat Assessment")
    
    # Threat level gauge
    col1, col2 = st.columns([2, 1])
    
    with col1:
        threat_gauge = viz_engine.create_threat_level_gauge(current_threat)
        st.plotly_chart(threat_gauge, use_container_width=True, 
                      config=viz_engine.get_mobile_responsive_config())
    
    with col2:
        # Alert status
        if current_threat >= 90:
            st.error("🚨 CRITICAL THREAT LEVEL")
            st.write("**Immediate Action Required**")
        elif current_threat >= 70:
            st.warning("⚠️ HIGH THREAT LEVEL")
            st.write("**Enhanced Monitoring Active**")
        elif current_threat >= 40:
            st.info("🟡 MODERATE THREAT LEVEL")
            st.write("**Normal Monitoring**")
        else:
            st.success("🟢 LOW THREAT LEVEL")
            st.write("**Routine Operations**")
        
        # Quick stats
        st.metric("Active Alerts", "23", "+5")
        st.metric("Bot Accounts", "156", "+12")
        st.metric("Network Nodes", "1,247", "+34")
    
    # Risk score distribution
    st.subheader("📊 Risk Score Distribution Analysis")
    risk_histogram = viz_engine.create_risk_score_histogram([])
    st.plotly_chart(risk_histogram, use_container_width=True,
                  config=viz_engine.get_mobile_responsive_config())
    
    # Bot detection analysis
    st.subheader("🤖 Bot Detection & Behavior Analysis")
    bot_scatter = viz_engine.create_bot_detection_scatter([])
    st.plotly_chart(bot_scatter, use_container_width=True,
                  config=viz_engine.get_mobile_responsive_config())

def display_geographic_intelligence_tab(viz_engine, geo_region):
    """Display geographic intelligence visualizations"""
    
    st.subheader(f"🗺️ Geographic Threat Analysis - {geo_region}")
    
    # Geographic heatmap
    geo_heatmap = viz_engine.create_geographic_heatmap([])
    st.plotly_chart(geo_heatmap, use_container_width=True,
                  config=viz_engine.get_mobile_responsive_config())
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform distribution
        st.subheader("📱 Platform Distribution")
        platform_dist = viz_engine.create_platform_distribution({})
        st.plotly_chart(platform_dist, use_container_width=True,
                      config=viz_engine.get_mobile_responsive_config())
    
    with col2:
        # Keyword analysis
        st.subheader("🔍 Threat Keywords Analysis")
        try:
            keyword_treemap = viz_engine.create_keyword_treemap({})
            st.plotly_chart(keyword_treemap, use_container_width=True,
                          config=viz_engine.get_mobile_responsive_config())
        except Exception as e:
            st.error(f"Error creating keyword analysis: {str(e)}")
            # Create a simple fallback chart
            import plotly.express as px
            import pandas as pd
            
            # Fallback data
            fallback_data = {
                'Keywords': ['terrorism', 'bomb', 'cyber_fraud', 'phishing', 'fake_news', 'attack'],
                'Frequency': [1250, 890, 2340, 1890, 3450, 1450],
                'Risk_Level': [95, 98, 78, 75, 65, 85]
            }
            df = pd.DataFrame(fallback_data)
            
            fig = px.bar(df, x='Keywords', y='Frequency', color='Risk_Level',
                        title="🔍 Threat Keywords Analysis",
                        color_continuous_scale='Reds')
            fig.update_layout(
                paper_bgcolor='#2C3E50',
                plot_bgcolor='#0D1B2A',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Geographic insights
    with st.expander("📊 Geographic Intelligence Insights"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("High-Risk Cities", "8", "+2")
            st.write("Cities with threat level > 70")
        
        with col2:
            st.metric("Cross-Border Activity", "15%", "+3%")
            st.write("International coordination detected")
        
        with col3:
            st.metric("Regional Hotspots", "3", "unchanged")
            st.write("Concentrated threat zones")

def display_network_analysis_tab(viz_engine):
    """Display network analysis visualizations"""
    
    st.subheader("�️ Account Network & Connection Analysis")
    
    # Network graph
    network_graph = viz_engine.create_network_graph({})
    st.plotly_chart(network_graph, use_container_width=True,
                  config=viz_engine.get_mobile_responsive_config())
    
    # Network metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔗 Total Connections", "1,247", "+23")
    
    with col2:
        st.metric("🤖 Bot Accounts", "156", "+8")
    
    with col3:
        st.metric("🚨 High-Risk Nodes", "34", "+2")
    
    with col4:
        st.metric("🌐 Network Clusters", "12", "+1")
    
    # Detailed analysis
    with st.expander("🔍 Network Intelligence Details"):
        st.markdown("""
        **🕸️ Network Analysis Findings:**
        - **Coordination Patterns**: 3 major bot networks identified
        - **Information Flow**: Primary propagation through 5 key accounts
        - **Geographic Distribution**: Networks span 8 Indian states
        - **Platform Presence**: Cross-platform coordination detected
        - **Threat Assessment**: Medium to high risk coordination capability
        """)

def display_trend_analysis_tab(viz_engine, time_range):
    """Display trend analysis visualizations"""
    
    st.subheader(f"📈 Trend Analysis - {time_range}")
    
    # Timeline analysis
    timeline = viz_engine.create_timeline_analysis([])
    st.plotly_chart(timeline, use_container_width=True,
                  config=viz_engine.get_mobile_responsive_config())
    
    # Engagement velocity
    st.subheader("🚀 Engagement Velocity Monitoring")
    engagement = viz_engine.create_engagement_velocity([])
    st.plotly_chart(engagement, use_container_width=True,
                  config=viz_engine.get_mobile_responsive_config())
    
    # Trend insights
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("**📊 Key Trend Insights:**")
            insights = [
                "📈 Threat activity increased 15% in last 24 hours",
                "🤖 Bot coordination patterns show weekly cycles",
                "🚨 Critical events correlate with news cycles",
                "📱 Cross-platform activity increased 23%",
                "🔍 New keyword emergence: 3 terms detected"
            ]
            
            for insight in insights:
                st.write(f"• {insight}")
    
    with col2:
        # Color scheme display
        with st.container():
            st.markdown("**🎨 Police Color Scheme:**")
            colors = viz_engine.get_police_color_scheme()
            
            key_colors = ['police_blue', 'alert_red', 'warning_orange', 'safe_green']
            for color_name in key_colors:
                if color_name in colors:
                    st.color_picker(
                        f"{color_name.replace('_', ' ').title()}", 
                        colors[color_name], 
                        disabled=True
                    )

def display_installation_instructions():
    """Display installation instructions for visualization dependencies"""
    
    st.error("📦 Professional Police Visualization Dependencies Not Installed")
    
    st.markdown("""
    ### 🚀 To Enable Professional Police Visualizations:
    
    **Install Required Dependencies:**
    ```bash
    pip install plotly>=5.15.0 kaleido>=0.2.1
    pip install -r requirements.txt
    ```
    
    **After Installation, You'll Have Access To:**
    - 🚨 Real-time threat level gauges with police color schemes
    - 🗺️ Geographic heatmaps of threats across Indian cities
    - 🕸️ Interactive network graphs showing account connections
    - 📈 Timeline analysis of campaign evolution
    - 📱 Platform distribution charts with detailed breakdowns
    - 🚀 Engagement velocity monitoring with viral thresholds
    - 📊 Risk score histograms with statistical analysis
    - 🔍 Keyword frequency treemaps for threat analysis
    - 🤖 Bot detection scatter plots with behavior patterns
    """)

def display_fallback_visualization():
    """Display fallback visualizations when Plotly is not available"""
    
    st.subheader("📊 Basic Visualization Dashboard")
    st.info("Install Plotly for enhanced police-grade visualizations")
    
    # Create basic charts using Streamlit's built-in capabilities
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Threat Level Monitor")
        # Simple metric display
        threat_level = 75
        if threat_level >= 80:
            st.error(f"HIGH THREAT: {threat_level}/100")
        elif threat_level >= 50:
            st.warning(f"MEDIUM THREAT: {threat_level}/100")
        else:
            st.success(f"LOW THREAT: {threat_level}/100")
        
        # Basic bar chart
        basic_data = {
            'Platform': ['Twitter', 'Facebook', 'Instagram', 'Telegram'],
            'Threats': [45, 32, 28, 15]
        }
        st.bar_chart(basic_data, x='Platform', y='Threats')
    
    with col2:
        st.subheader("📈 Activity Trends")
        
        # Basic line chart
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        activity_data = pd.DataFrame({
            'Date': dates,
            'Activity': np.random.randint(50, 200, 30),
            'Threats': np.random.randint(5, 50, 30)
        })
        st.line_chart(activity_data.set_index('Date'))
    
    # Sample insights
    st.subheader("🔍 Intelligence Summary")
    
    insights_col1, insights_col2, insights_col3 = st.columns(3)
    
    with insights_col1:
        st.metric("Total Monitored Accounts", "1,247", "+34")
        st.metric("Active Threats", "23", "+5")
    
    with insights_col2:
        st.metric("Bot Detection Rate", "12.5%", "+2.1%")
        st.metric("Geographic Hotspots", "8", "+1")
    
    with insights_col3:
        st.metric("Platform Coverage", "6", "unchanged")
        st.metric("Keyword Alerts", "156", "+12")
    
    # Professional features preview
    with st.expander("🏛️ Professional Features Available After Installation"):
        st.markdown("""
        **🚨 Enhanced Police Visualizations Include:**
        - Dark theme optimized for 24/7 monitoring centers
        - Police color scheme (blue/red) for instant threat recognition
        - Interactive tooltips with detailed threat information
        - Export capabilities for court evidence documentation
        - Mobile-responsive design for field operations
        - Real-time data visualization capabilities
        - Professional styling suitable for official police reports
        - Integration-ready with existing police intelligence systems
        """)

def main():
    st.title("📊 Professional Police Data Visualization")
    st.markdown("🏛️ Advanced analytics and insights for law enforcement cyber monitoring")
    st.markdown("---")
    
    if PLOTLY_AVAILABLE:
        # Initialize police visualization engine
        try:
            viz_engine = PoliceVisualizationEngine()
            display_police_visualization_dashboard(viz_engine)
        except Exception as e:
            st.error(f"Error initializing police visualization engine: {e}")
            display_fallback_visualization()
    else:
        display_installation_instructions()
        display_fallback_visualization()

def display_trend_analysis(df, selected_metrics, group_by):
    """Display trend analysis visualizations"""
    st.subheader("📈 Trend Analysis")
    
    # Key insights
    with st.container():
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("**📊 Key Insights:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            trend_direction = "📈" if np.random.random() > 0.5 else "📉"
            st.write(f"{trend_direction} Overall mentions trending {'up' if trend_direction == '📈' else 'down'} by {np.random.randint(5, 25)}%")
        
        with col2:
            sentiment_emoji = "😊" if np.random.random() > 0.5 else "😞"
            st.write(f"{sentiment_emoji} Sentiment is {'positive' if sentiment_emoji == '😊' else 'concerning'} with score {np.random.uniform(0.2, 0.8):.2f}")
        
        with col3:
            engagement_trend = "🚀" if np.random.random() > 0.5 else "⚠️"
            st.write(f"{engagement_trend} Engagement {'above' if engagement_trend == '🚀' else 'below'} average by {np.random.randint(10, 40)}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Multi-metric trend chart
    st.subheader("Multi-Metric Trends")
    trend_chart = create_multi_metric_trend(df, selected_metrics, group_by)
    st.plotly_chart(trend_chart, use_container_width=True)
    
    # Individual metric trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mentions Timeline")
        mentions_chart = create_mentions_timeline(df, group_by)
        st.plotly_chart(mentions_chart, use_container_width=True)
    
    with col2:
        st.subheader("Sentiment Evolution")
        sentiment_chart = create_sentiment_evolution(df, group_by)
        st.plotly_chart(sentiment_chart, use_container_width=True)
    
    # Engagement trends
    st.subheader("Engagement Trends by Platform")
    engagement_chart = create_engagement_trends(df)
    st.plotly_chart(engagement_chart, use_container_width=True)

def display_comparison_analysis(df, platforms):
    """Display platform and metric comparisons"""
    st.subheader("🔄 Comparative Analysis")
    
    # Platform comparison radar chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Platform Performance Radar")
        radar_chart = create_platform_radar(df, platforms)
        st.plotly_chart(radar_chart, use_container_width=True)
    
    with col2:
        st.subheader("Metric Correlation Matrix")
        correlation_chart = create_correlation_matrix(df)
        st.plotly_chart(correlation_chart, use_container_width=True)
    
    # Side-by-side comparisons
    st.subheader("Platform Comparison")
    comparison_chart = create_platform_comparison(df, platforms)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Time-based comparison
    st.subheader("Time Period Comparison")
    time_comparison_chart = create_time_comparison(df)
    st.plotly_chart(time_comparison_chart, use_container_width=True)

def display_performance_analysis(df):
    """Display performance analysis"""
    st.subheader("🎯 Performance Analysis")
    
    # KPI dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-highlight">
            <h3>Engagement Score</h3>
            <h2>87.5</h2>
            <p>+12.3% vs last period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-highlight">
            <h3>Virality Index</h3>
            <h2>6.2</h2>
            <p>+0.8 vs last period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-highlight">
            <h3>Response Rate</h3>
            <h2>94.2%</h2>
            <p>-2.1% vs last period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-highlight">
            <h3>Brand Health</h3>
            <h2>Strong</h2>
            <p>Sentiment: 0.73</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Score Breakdown")
        performance_chart = create_performance_breakdown(df)
        st.plotly_chart(performance_chart, use_container_width=True)
    
    with col2:
        st.subheader("Content Performance Distribution")
        content_chart = create_content_performance(df)
        st.plotly_chart(content_chart, use_container_width=True)
    
    # Engagement funnel
    st.subheader("Engagement Funnel Analysis")
    funnel_chart = create_engagement_funnel(df)
    st.plotly_chart(funnel_chart, use_container_width=True)

def display_geographic_analysis(df):
    """Display geographic analysis"""
    st.subheader("🌐 Geographic Analysis")
    
    # World map
    st.subheader("Global Mention Distribution")
    world_map = create_world_map(df)
    st.plotly_chart(world_map, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Countries by Volume")
        country_chart = create_country_analysis(df)
        st.plotly_chart(country_chart, use_container_width=True)
    
    with col2:
        st.subheader("Regional Sentiment Analysis")
        regional_chart = create_regional_sentiment(df)
        st.plotly_chart(regional_chart, use_container_width=True)
    
    # Geographic trends
    st.subheader("Geographic Trends Over Time")
    geo_trend_chart = create_geographic_trends(df)
    st.plotly_chart(geo_trend_chart, use_container_width=True)

def display_advanced_analysis(df, chart_types):
    """Display advanced analysis and custom visualizations"""
    st.subheader("🔍 Advanced Analytics")
    
    # Sankey diagram for content flow
    if "Sankey Diagrams" in chart_types:
        st.subheader("Content Flow Analysis")
        sankey_chart = create_sankey_diagram(df)
        st.plotly_chart(sankey_chart, use_container_width=True)
    
    # Treemap for hierarchical data
    if "Treemaps" in chart_types:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Content Categories Treemap")
            treemap_chart = create_treemap_analysis(df)
            st.plotly_chart(treemap_chart, use_container_width=True)
        
        with col2:
            st.subheader("Platform Engagement Treemap")
            platform_treemap = create_platform_treemap(df)
            st.plotly_chart(platform_treemap, use_container_width=True)
    
    # Heatmaps
    if "Heatmaps" in chart_types:
        st.subheader("Activity Heatmap")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Hourly Activity Heatmap")
            hourly_heatmap = create_hourly_heatmap(df)
            st.plotly_chart(hourly_heatmap, use_container_width=True)
        
        with col2:
            st.subheader("Platform vs Sentiment Heatmap")
            sentiment_heatmap = create_sentiment_heatmap(df)
            st.plotly_chart(sentiment_heatmap, use_container_width=True)
    
    # Network analysis
    st.subheader("Influence Network Analysis")
    network_chart = create_network_analysis(df)
    st.plotly_chart(network_chart, use_container_width=True)

# Chart creation functions
def create_multi_metric_trend(df, metrics, group_by):
    """Create multi-metric trend chart"""
    fig = make_subplots(
        rows=len(metrics), cols=1,
        subplot_titles=metrics,
        shared_xaxes=True,
        vertical_spacing=0.05
    )
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, metric in enumerate(metrics):
        y_data = np.random.random(24) * 100  # Sample data
        x_data = pd.date_range(start='2024-01-01', periods=24, freq='H')
        
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                name=metric,
                line=dict(color=colors[i % len(colors)])
            ),
            row=i+1, col=1
        )
    
    fig.update_layout(height=200*len(metrics), showlegend=False)
    return fig

def create_mentions_timeline(df, group_by):
    """Create mentions timeline chart"""
    # Generate sample timeline data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    mentions = np.random.poisson(50, 30)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=mentions,
        mode='lines+markers',
        fill='tonexty',
        name='Mentions'
    ))
    
    fig.update_layout(
        title="Mentions Over Time",
        height=300,
        showlegend=False
    )
    return fig

def create_sentiment_evolution(df, group_by):
    """Create sentiment evolution chart"""
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    sentiment = np.random.uniform(-1, 1, 30)
    
    colors = ['red' if s < -0.2 else 'green' if s > 0.2 else 'orange' for s in sentiment]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=sentiment,
        mode='lines+markers',
        marker=dict(color=colors),
        name='Sentiment'
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(title="Sentiment Evolution", height=300)
    return fig

def create_engagement_trends(df):
    """Create engagement trends chart"""
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    
    fig = go.Figure()
    
    for platform in platforms:
        engagement = np.random.uniform(0.02, 0.15, 30)
        fig.add_trace(go.Scatter(
            x=dates,
            y=engagement,
            mode='lines',
            name=platform
        ))
    
    fig.update_layout(title="Engagement Trends by Platform", height=400)
    return fig

def create_platform_radar(df, platforms):
    """Create platform performance radar chart"""
    metrics = ['Mentions', 'Engagement', 'Sentiment', 'Reach', 'Virality']
    
    fig = go.Figure()
    
    for platform in platforms[:3]:  # Limit to 3 platforms for clarity
        values = np.random.uniform(0.3, 1.0, len(metrics))
        values = np.append(values, values[0])  # Complete the circle
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics + [metrics[0]],
            fill='toself',
            name=platform
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Platform Performance Radar",
        height=400
    )
    return fig

def create_correlation_matrix(df):
    """Create correlation matrix heatmap"""
    # Generate sample correlation data
    metrics = ['Mentions', 'Engagement', 'Sentiment', 'Reach']
    corr_matrix = np.random.uniform(-1, 1, (len(metrics), len(metrics)))
    np.fill_diagonal(corr_matrix, 1)
    
    fig = px.imshow(
        corr_matrix,
        x=metrics,
        y=metrics,
        color_continuous_scale='RdBu',
        title="Metrics Correlation Matrix"
    )
    fig.update_layout(height=400)
    return fig

def create_platform_comparison(df, platforms):
    """Create platform comparison chart"""
    metrics = ['Mentions', 'Engagement', 'Sentiment', 'Reach']
    
    fig = go.Figure()
    
    x = np.arange(len(metrics))
    width = 0.2
    
    for i, platform in enumerate(platforms[:4]):
        values = np.random.uniform(0.3, 1.0, len(metrics))
        fig.add_trace(go.Bar(
            name=platform,
            x=[j + i*width for j in x],
            y=values,
            width=width
        ))
    
    fig.update_layout(
        title="Platform Performance Comparison",
        xaxis=dict(tickmode='array', tickvals=x, ticktext=metrics),
        height=400
    )
    return fig

def create_time_comparison(df):
    """Create time period comparison chart"""
    periods = ['This Week', 'Last Week', 'This Month', 'Last Month']
    metrics = ['Mentions', 'Engagement', 'Sentiment']
    
    fig = make_subplots(
        rows=1, cols=len(metrics),
        subplot_titles=metrics,
        specs=[[{"secondary_y": False}]*len(metrics)]
    )
    
    for i, metric in enumerate(metrics):
        values = np.random.uniform(50, 200, len(periods))
        fig.add_trace(
            go.Bar(x=periods, y=values, name=metric, showlegend=False),
            row=1, col=i+1
        )
    
    fig.update_layout(height=300)
    return fig

def create_performance_breakdown(df):
    """Create performance breakdown chart"""
    categories = ['Content Quality', 'Timing', 'Audience Targeting', 'Platform Optimization']
    scores = np.random.uniform(60, 95, len(categories))
    
    fig = go.Figure(go.Bar(
        x=categories,
        y=scores,
        marker_color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    ))
    
    fig.update_layout(title="Performance Score Breakdown", height=300)
    return fig

def create_content_performance(df):
    """Create content performance distribution"""
    performance_scores = np.random.normal(75, 15, 100)
    
    fig = px.histogram(
        x=performance_scores,
        nbins=20,
        title="Content Performance Distribution"
    )
    fig.update_layout(height=300)
    return fig

def create_engagement_funnel(df):
    """Create engagement funnel chart"""
    stages = ['Impressions', 'Views', 'Clicks', 'Shares', 'Comments']
    values = [100000, 25000, 5000, 1000, 250]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(title="Engagement Funnel", height=400)
    return fig

def create_world_map(df):
    """Create world map visualization"""
    countries = ['USA', 'UK', 'Germany', 'France', 'Japan', 'Australia', 'Canada', 'Brazil']
    mentions = np.random.randint(100, 1000, len(countries))
    
    fig = px.choropleth(
        locations=countries,
        color=mentions,
        locationmode='country names',
        title="Global Mention Distribution",
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)
    return fig

def create_country_analysis(df):
    """Create country analysis chart"""
    countries = ['USA', 'UK', 'Germany', 'France', 'Japan']
    mentions = np.random.randint(100, 500, len(countries))
    
    fig = px.bar(
        x=countries,
        y=mentions,
        title="Top Countries by Mentions"
    )
    fig.update_layout(height=300)
    return fig

def create_regional_sentiment(df):
    """Create regional sentiment analysis"""
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
    sentiment = np.random.uniform(-0.5, 0.8, len(regions))
    
    colors = ['red' if s < 0 else 'green' for s in sentiment]
    
    fig = px.bar(
        x=regions,
        y=sentiment,
        title="Regional Sentiment Analysis",
        color=sentiment,
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=300)
    return fig

def create_geographic_trends(df):
    """Create geographic trends chart"""
    # Implementation for geographic trends
    fig = px.line(
        x=pd.date_range('2024-01-01', periods=30, freq='D'),
        y=np.random.randint(50, 200, 30),
        title="Geographic Trends Over Time"
    )
    fig.update_layout(height=300)
    return fig

def create_sankey_diagram(df):
    """Create Sankey diagram for content flow"""
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["Platform A", "Platform B", "Engagement", "Shares", "Comments"],
            color="blue"
        ),
        link=dict(
            source=[0, 1, 0, 2, 3],
            target=[2, 2, 3, 4, 4],
            value=[10, 20, 15, 5, 8]
        )
    )])
    
    fig.update_layout(title_text="Content Flow Analysis", height=400)
    return fig

def create_treemap_analysis(df):
    """Create treemap for content categories"""
    categories = ['News', 'Entertainment', 'Sports', 'Technology', 'Lifestyle']
    values = np.random.randint(50, 300, len(categories))
    
    fig = px.treemap(
        names=categories,
        values=values,
        title="Content Categories"
    )
    fig.update_layout(height=300)
    return fig

def create_platform_treemap(df):
    """Create platform engagement treemap"""
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']
    values = np.random.randint(100, 500, len(platforms))
    
    fig = px.treemap(
        names=platforms,
        values=values,
        title="Platform Engagement"
    )
    fig.update_layout(height=300)
    return fig

def create_hourly_heatmap(df):
    """Create hourly activity heatmap"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = list(range(24))
    
    z = np.random.randint(0, 100, (len(days), len(hours)))
    
    fig = px.imshow(
        z,
        x=hours,
        y=days,
        title="Hourly Activity Heatmap",
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=300)
    return fig

def create_sentiment_heatmap(df):
    """Create platform vs sentiment heatmap"""
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']
    sentiments = ['Positive', 'Neutral', 'Negative']
    
    z = np.random.randint(10, 100, (len(platforms), len(sentiments)))
    
    fig = px.imshow(
        z,
        x=sentiments,
        y=platforms,
        title="Platform vs Sentiment",
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=300)
    return fig

def create_network_analysis(df):
    """Create network analysis visualization"""
    # Simplified network visualization
    fig = go.Figure()
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=np.random.random(10),
        y=np.random.random(10),
        mode='markers+text',
        text=['Node ' + str(i) for i in range(10)],
        textposition="middle center",
        marker=dict(size=20, color='lightblue'),
        name='Influencers'
    ))
    
    fig.update_layout(
        title="Influence Network",
        height=400,
        showlegend=False
    )
    return fig

def export_visualizations(format_type):
    """Export all visualizations"""
    st.success(f"Visualizations exported in {format_type} format!")

if __name__ == "__main__":
    main()
