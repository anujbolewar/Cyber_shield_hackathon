#!/usr/bin/env python3
"""
🏠 DASHBOARD - POLICE AI MONITORING SYSTEM
Professional dashboard with comprehensive feature access
Government-style interface for law enforcement operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

# Page configuration
st.set_page_config(
    page_title="Police AI Monitor Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for Government-style Dashboard
st.markdown("""
<style>
    /* Government Dashboard Theme */
    :root {
        --gov-blue: #1e3a8a;
        --gov-blue-dark: #1e40af;
        --gov-blue-light: #3b82f6;
        --gov-accent: #fbbf24;
        --gov-red: #dc2626;
        --gov-green: #16a34a;
        --gov-gray: #6b7280;
        --gov-white: #ffffff;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Header styling */
    .gov-header {
        background: linear-gradient(135deg, var(--gov-blue) 0%, var(--gov-blue-dark) 100%);
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        position: relative;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .gov-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--gov-red) 0%, var(--gov-accent) 50%, var(--gov-green) 100%);
    }
    
    .header-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        font-size: 16px;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        text-align: center;
    }
    
    /* Navigation Cards */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .nav-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .nav-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
        border-color: var(--gov-blue-light);
    }
    
    .nav-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gov-blue);
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .nav-card:hover::before {
        transform: translateX(0);
    }
    
    .nav-icon {
        font-size: 48px;
        margin-bottom: 1rem;
        display: block;
    }
    
    .nav-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--gov-blue);
        margin-bottom: 0.5rem;
    }
    
    .nav-description {
        font-size: 14px;
        color: var(--gov-gray);
        line-height: 1.4;
    }
    
    /* Status indicators */
    .status-online {
        color: var(--gov-green);
    }
    
    .status-warning {
        color: var(--gov-accent);
    }
    
    .status-offline {
        color: var(--gov-red);
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stat-number {
        font-size: 32px;
        font-weight: 700;
        color: var(--gov-blue);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 14px;
        color: var(--gov-gray);
        font-weight: 500;
    }
    
    /* Quick actions */
    .quick-action-btn {
        background: linear-gradient(135deg, var(--gov-blue) 0%, var(--gov-blue-dark) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        margin: 0.25rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.3);
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.4);
    }
    
    /* User info */
    .user-info {
        background: linear-gradient(135deg, var(--gov-blue) 0%, var(--gov-blue-dark) 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Recent activity */
    .activity-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--gov-blue);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .nav-grid {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .header-title {
            font-size: 24px;
        }
        
        .nav-icon {
            font-size: 36px;
        }
    }
</style>
""", unsafe_allow_html=True)

def initialize_dashboard_state():
    """Initialize dashboard session state"""
    if 'dashboard_initialized' not in st.session_state:
        st.session_state.dashboard_initialized = True
        st.session_state.user_authenticated = True  # Assume authenticated for dashboard access
        st.session_state.current_user = {
            'name': 'Officer Johnson',
            'badge': 'PD-2024-001',
            'department': 'Intelligence Division',
            'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def get_system_statistics():
    """Get system statistics for dashboard"""
    # Mock statistics - in real implementation, these would come from database
    stats = {
        'active_alerts': 3,
        'monitored_feeds': 12,
        'api_connections': 5,
        'scraped_data': 1247,
        'intelligence_reports': 89,
        'evidence_items': 156,
        'uptime_hours': 24 * 7,  # 7 days
        'processed_nlp': 3421
    }
    return stats

def display_header():
    """Display government-style header"""
    st.markdown("""
    <div class="gov-header">
        <div class="header-title">
            🚔 POLICE AI MONITORING SYSTEM
        </div>
        <div class="header-subtitle">
            Department of Law Enforcement • Intelligence Operations Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_user_info():
    """Display current user information"""
    user = st.session_state.current_user
    
    st.markdown(f"""
    <div class="user-info">
        <h4 style="margin: 0 0 0.5rem 0;">👮 Welcome, {user['name']}</h4>
        <p style="margin: 0; opacity: 0.9;">
            Badge: {user['badge']} | {user['department']}<br>
            Last Login: {user['last_login']}
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_system_stats():
    """Display system statistics"""
    st.markdown("### 📊 System Overview")
    
    stats = get_system_statistics()
    
    # Create stats grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number status-warning">{stats['active_alerts']}</div>
            <div class="stat-label">Active Alerts</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number status-online">{stats['monitored_feeds']}</div>
            <div class="stat-label">Monitored Feeds</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number status-online">{stats['api_connections']}</div>
            <div class="stat-label">API Connections</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['scraped_data']:,}</div>
            <div class="stat-label">Scraped Data Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['intelligence_reports']}</div>
            <div class="stat-label">Intelligence Reports</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['evidence_items']}</div>
            <div class="stat-label">Evidence Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number status-online">{stats['uptime_hours']}</div>
            <div class="stat-label">Uptime Hours</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['processed_nlp']:,}</div>
            <div class="stat-label">NLP Processed</div>
        </div>
        """, unsafe_allow_html=True)

def display_navigation_grid():
    """Display main navigation grid with all system features"""
    st.markdown("### 🎯 System Features")
    
    # Navigation items matching the sidebar features
    nav_items = [
        {
            'icon': '📡',
            'title': 'Real Time Feed',
            'description': 'Live monitoring of intelligence feeds and data streams',
            'page': 'pages/1_📡_Real_Time_Feed.py',
            'status': 'online'
        },
        {
            'icon': '🚨',
            'title': 'Alert System',
            'description': 'Advanced threat detection and alert management',
            'page': 'pages/2_🚨_Alert_System.py',
            'status': 'warning'
        },
        {
            'icon': '📊',
            'title': 'Data Visualization',
            'description': 'Analytics dashboards and intelligence charts',
            'page': 'pages/3_📊_Data_Visualization.py',
            'status': 'online'
        },
        {
            'icon': '🔑',
            'title': 'API Management',
            'description': 'Configure and test API connections',
            'page': 'pages/4_🔑_API_Management.py',
            'status': 'online'
        },
        {
            'icon': '🎯',
            'title': 'Intelligence Operations',
            'description': 'OSINT and intelligence analysis tools',
            'page': 'pages/5_🎯_Intelligence_Operations.py',
            'status': 'online'
        },
        {
            'icon': '🧠',
            'title': 'NLP Analysis',
            'description': 'Natural language processing and text analysis',
            'page': 'pages/6_🧠_NLP_Analysis.py',
            'status': 'online'
        },
        {
            'icon': '🌐',
            'title': 'Web Scraper',
            'description': 'Advanced web scraping for intelligence gathering',
            'page': 'pages/10_🌐_Web_Scraper.py',
            'status': 'online'
        },
        {
            'icon': '🐦',
            'title': 'Live Twitter Monitor',
            'description': 'Real-time social media surveillance',
            'page': 'utils/twitter_monitor.py',
            'status': 'online'
        },
        {
            'icon': '📚',
            'title': 'Legal Evidence Manager',
            'description': 'Court-ready evidence collection and management',
            'page': 'utils/legal_evidence_manager.py',
            'status': 'online'
        },
        {
            'icon': '🚀',
            'title': 'Deployment Manager',
            'description': 'Multi-platform deployment and configuration',
            'page': 'utils/deployment_strategies.py',
            'status': 'online'
        },
        {
            'icon': '🔧',
            'title': 'System Configuration',
            'description': 'System settings and maintenance tools',
            'page': '#',
            'status': 'online'
        },
        {
            'icon': '📋',
            'title': 'Reports & Analytics',
            'description': 'Generate intelligence reports and analytics',
            'page': '#',
            'status': 'online'
        }
    ]
    
    # Create navigation grid
    cols = st.columns(3)
    
    for i, item in enumerate(nav_items):
        with cols[i % 3]:
            status_class = f"status-{item['status']}" if item['status'] != 'online' else ""
            
            # Create clickable card
            if st.button(
                f"{item['icon']} {item['title']}", 
                key=f"nav_{i}",
                help=item['description'],
                use_container_width=True
            ):
                if item['page'] != '#':
                    st.switch_page(item['page'])
                else:
                    st.info(f"🚧 {item['title']} feature coming soon!")
            
            # Description below button
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem; padding: 0 0.5rem;">
                <small style="color: #6b7280;">{item['description']}</small>
            </div>
            """, unsafe_allow_html=True)

def display_quick_actions():
    """Display quick action buttons"""
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Start Investigation", use_container_width=True, type="primary"):
            st.switch_page("pages/5_🎯_Intelligence_Operations.py")
    
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/3_📊_Data_Visualization.py")
    
    with col3:
        if st.button("🚨 Check Alerts", use_container_width=True):
            st.switch_page("pages/2_🚨_Alert_System.py")
    
    with col4:
        if st.button("🌐 Web Scraping", use_container_width=True):
            st.switch_page("pages/10_🌐_Web_Scraper.py")

def display_recent_activity():
    """Display recent system activity"""
    st.markdown("### 📋 Recent Activity")
    
    # Mock recent activity data
    activities = [
        {
            'time': '2 minutes ago',
            'action': 'New alert generated',
            'details': 'Suspicious social media activity detected',
            'type': 'alert'
        },
        {
            'time': '15 minutes ago',
            'action': 'Web scraping completed',
            'details': '247 news articles processed',
            'type': 'scraping'
        },
        {
            'time': '1 hour ago',
            'action': 'API connection tested',
            'details': 'OpenAI API successfully validated',
            'type': 'api'
        },
        {
            'time': '2 hours ago',
            'action': 'Evidence uploaded',
            'details': 'Digital evidence added to case #2024-001',
            'type': 'evidence'
        },
        {
            'time': '3 hours ago',
            'action': 'Intelligence report generated',
            'details': 'Weekly threat assessment completed',
            'type': 'report'
        }
    ]
    
    for activity in activities:
        icon_map = {
            'alert': '🚨',
            'scraping': '🌐',
            'api': '🔑',
            'evidence': '📚',
            'report': '📋'
        }
        
        st.markdown(f"""
        <div class="activity-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{icon_map.get(activity['type'], '📄')} {activity['action']}</strong><br>
                    <small style="color: #6b7280;">{activity['details']}</small>
                </div>
                <div style="text-align: right; color: #6b7280; font-size: 12px;">
                    {activity['time']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_system_health():
    """Display system health indicators"""
    st.markdown("### 🏥 System Health")
    
    # System health metrics
    health_metrics = {
        'CPU Usage': 45,
        'Memory Usage': 62,
        'Disk Usage': 34,
        'Network': 89
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for metric, value in list(health_metrics.items())[:2]:
            # Color coding based on usage
            if value < 50:
                color = "#16a34a"  # Green
            elif value < 80:
                color = "#fbbf24"  # Yellow
            else:
                color = "#dc2626"  # Red
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': metric},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        for metric, value in list(health_metrics.items())[2:]:
            # Color coding based on usage
            if value < 50:
                color = "#16a34a"  # Green
            elif value < 80:
                color = "#fbbf24"  # Yellow
            else:
                color = "#dc2626"  # Red
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': metric},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

def main():
    """Main dashboard application"""
    initialize_dashboard_state()
    
    # Check authentication (in real implementation, this would be more robust)
    if not st.session_state.get('user_authenticated', False):
        st.error("🔒 Access Denied. Please authenticate to access the dashboard.")
        st.stop()
    
    # Display header
    display_header()
    
    # Main dashboard layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # System statistics
        display_system_stats()
        
        # Navigation grid
        display_navigation_grid()
        
        # Quick actions
        display_quick_actions()
    
    with col2:
        # User information
        display_user_info()
        
        # System health
        display_system_health()
        
        # Recent activity
        display_recent_activity()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 1rem;">
        <p><strong>Police AI Monitoring System</strong> | Version 2.0 | Designed for Law Enforcement Operations</p>
        <p>🔒 Secure • 🚀 Real-time • 🎯 Intelligence-driven</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
