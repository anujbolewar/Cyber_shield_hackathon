import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import json
import random

# Page configuration
st.set_page_config(
    page_title="Police AI Monitor - Law Enforcement Intelligence Platform",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for police theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚔 Police AI Monitor</h1>
        <p>Law Enforcement Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔐 Navigation")
    page = st.sidebar.selectbox("Select Page", [
        "🏠 Dashboard",
        "📡 Real-Time Feed", 
        "🚨 Alert System",
        "📊 Data Visualization",
        "🔑 API Management",
        "🧠 NLP Analysis",
        "🌐 Web Scraper",
        "⚖️ Evidence Manager"
    ])
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📡 Real-Time Feed":
        show_realtime_feed()
    elif page == "🚨 Alert System":
        show_alert_system()
    elif page == "📊 Data Visualization":
        show_data_visualization()
    elif page == "🔑 API Management":
        show_api_management()
    elif page == "🧠 NLP Analysis":
        show_nlp_analysis()
    elif page == "🌐 Web Scraper":
        show_web_scraper()
    elif page == "⚖️ Evidence Manager":
        show_evidence_manager()

def show_dashboard():
    st.header("🏠 System Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Alerts", "12", "↑ +3")
    with col2:
        st.metric("Monitored Feeds", "1,247", "↑ +156")
    with col3:
        st.metric("Threat Level", "MEDIUM", "↓ -1")
    with col4:
        st.metric("Evidence Items", "3,421", "↑ +89")
    
    # Sample chart
    st.subheader("📊 Alert Trends")
    dates = pd.date_range(start='2025-08-01', periods=30, freq='D')
    alerts = np.random.randint(5, 25, 30)
    
    fig = px.line(x=dates, y=alerts, title="Daily Alerts Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Alerts")
    st.plotly_chart(fig, use_container_width=True)

def show_realtime_feed():
    st.header("📡 Real-Time Intelligence Feed")
    st.info("🔴 Live monitoring active - Demo mode")
    
    # Sample real-time data
    for i in range(5):
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**Post {i+1}:** Sample social media content for demonstration...")
            with col2:
                sentiment = random.choice(["Positive", "Neutral", "Negative"])
                color = {"Positive": "green", "Neutral": "blue", "Negative": "red"}[sentiment]
                st.markdown(f"<span style='color: {color}'>{sentiment}</span>", unsafe_allow_html=True)
            with col3:
                threat = random.choice(["LOW", "MEDIUM", "HIGH"])
                st.write(f"Threat: {threat}")
        st.divider()

def show_alert_system():
    st.header("🚨 Alert Management System")
    
    st.success("✅ 3 Active Alerts")
    st.warning("⚠️ 1 Medium Priority Alert")
    st.error("🚨 0 Critical Alerts")
    
    # Sample alerts
    alerts_data = {
        "Time": ["10:30 AM", "11:45 AM", "02:15 PM"],
        "Type": ["Suspicious Activity", "Keyword Match", "Geographic Alert"],
        "Priority": ["High", "Medium", "Low"],
        "Status": ["Active", "Investigating", "Resolved"]
    }
    
    df = pd.DataFrame(alerts_data)
    st.dataframe(df, use_container_width=True)

def show_data_visualization():
    st.header("📊 Data Visualization & Analytics")
    
    # Sample charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        labels = ['Twitter', 'Facebook', 'Instagram', 'Other']
        values = [45, 25, 20, 10]
        fig = px.pie(values=values, names=labels, title="Platform Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar chart
        platforms = ['Twitter', 'Facebook', 'Instagram', 'YouTube']
        posts = [1200, 800, 600, 400]
        fig = px.bar(x=platforms, y=posts, title="Posts by Platform")
        st.plotly_chart(fig, use_container_width=True)

def show_api_management():
    st.header("🔑 API Management Center")
    
    st.info("🔒 Secure API configuration for external services")
    
    # API Status
    apis = {
        "Twitter/X API": "🟢 Connected",
        "Facebook API": "🟡 Limited",
        "Instagram API": "🔴 Disconnected",
        "YouTube API": "🟢 Connected"
    }
    
    for api, status in apis.items():
        st.write(f"**{api}:** {status}")
    
    st.button("🔄 Refresh Connections")
    st.button("⚙️ Configure APIs")

def show_nlp_analysis():
    st.header("🧠 NLP Analysis Engine")
    
    st.write("**Enter text for analysis:**")
    text_input = st.text_area("Text to analyze", "Enter text here for sentiment and threat analysis...")
    
    if st.button("🔍 Analyze Text"):
        if text_input:
            # Simulate NLP analysis
            sentiment_score = random.uniform(-1, 1)
            threat_level = random.choice(["LOW", "MEDIUM", "HIGH"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sentiment Score", f"{sentiment_score:.2f}")
            with col2:
                st.metric("Threat Level", threat_level)
            
            st.success("✅ Analysis complete!")

def show_web_scraper():
    st.header("🌐 Web Scraper")
    
    st.write("**URL to scrape:**")
    url = st.text_input("Enter website URL", "https://example.com")
    
    # Simple URL validation
    def is_valid_url(url):
        try:
            import re
            pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return pattern.match(url) is not None
        except:
            return True  # If validation fails, assume URL is valid
    
    scrape_type = st.selectbox("Content Type", [
        "News Articles",
        "Social Media Posts", 
        "Forum Discussions"
    ])
    
    if st.button("🕷️ Start Scraping"):
        if url and is_valid_url(url):
            with st.spinner("Scraping in progress..."):
                time.sleep(2)  # Simulate scraping
            st.success(f"✅ Successfully scraped content from {url}")
            
            # Sample results
            st.write("**Scraped Data:**")
            sample_data = {
                "Title": ["Sample Article 1", "Sample Article 2"],
                "Content": ["Sample content...", "More sample content..."],
                "Timestamp": ["2025-09-01 10:30", "2025-09-01 11:45"]
            }
            st.dataframe(pd.DataFrame(sample_data))
        elif url:
            st.error("❌ Please enter a valid URL starting with http:// or https://")
        else:
            st.warning("⚠️ Please enter a URL to scrape")

def show_evidence_manager():
    st.header("⚖️ Legal Evidence Manager")
    
    st.info("📁 Digital evidence collection and management")
    
    # Evidence stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Evidence Items", "156")
    with col2:
        st.metric("Cases", "23")
    with col3:
        st.metric("Verified Items", "142")
    
    # Sample evidence table
    evidence_data = {
        "Case ID": ["CASE_001", "CASE_002", "CASE_003"],
        "Type": ["Social Media Post", "Web Content", "Message"],
        "Date": ["2025-09-01", "2025-08-30", "2025-08-28"],
        "Status": ["Verified", "Pending", "Verified"]
    }
    
    st.dataframe(pd.DataFrame(evidence_data), use_container_width=True)
    
    if st.button("📥 Export Evidence Package"):
        st.success("✅ Evidence package exported successfully!")

if __name__ == "__main__":
    main()
