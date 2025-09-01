import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import sys
import os
from pathlib import Path

# Add project root to path for imports
current_dir = Path(__file__).parent.parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from core.alerts import AlertManager, AlertRule
from core.notifications import send_notification

st.set_page_config(
    page_title="Alert System - Police AI Monitor",
    page_icon="🚨",
    layout="wide"
)

# Enhanced Police Theme CSS for Alert System
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
    
    /* Alert system header */
    .alert-system-header {
        background: linear-gradient(135deg, var(--police-red) 0%, #b91c1c 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(220, 38, 38, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .alert-system-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, white 0%, var(--police-accent) 50%, white 100%);
        animation: alert-sweep 2s infinite linear;
    }
    
    @keyframes alert-sweep {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Enhanced alert cards */
    .alert-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid var(--police-red);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3);
        animation: alert-critical-pulse 2s infinite;
        position: relative;
        overflow: hidden;
    }
    
    .alert-critical::before {
        content: '🚨';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        animation: rotate 2s linear infinite;
    }
    
    @keyframes alert-critical-pulse {
        0% { transform: scale(1); box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3); }
        50% { transform: scale(1.02); box-shadow: 0 8px 25px rgba(220, 38, 38, 0.5); }
        100% { transform: scale(1); box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .alert-high {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid var(--police-accent);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
        position: relative;
    }
    
    .alert-high::before {
        content: '⚠️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.2rem;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        border: 2px solid var(--police-blue-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        position: relative;
    }
    
    .alert-medium::before {
        content: 'ℹ️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.2rem;
    }
    
    .alert-low {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border: 2px solid var(--police-green);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
        position: relative;
    }
    
    .alert-low::before {
        content: '✅';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.2rem;
    }
    
    /* Alert status indicators */
    .alert-status {
        display: inline-flex;
        align-items: center;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-active { 
        background: var(--police-red); 
        color: white; 
        animation: pulse-status 1.5s infinite;
    }
    .status-resolved { 
        background: var(--police-green); 
        color: white; 
    }
    .status-snoozed { 
        background: var(--police-accent); 
        color: black; 
    }
    
    @keyframes pulse-status {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Enhanced rule cards */
    .rule-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .rule-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(30, 58, 138, 0.15);
    }
    
    .rule-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--police-blue);
        border-radius: 2px 0 0 2px;
    }
    
    /* Dashboard metrics */
    .alert-dashboard {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.3);
    }
    
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .dashboard-metric {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .dashboard-metric:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    .dashboard-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--police-accent);
        margin-bottom: 0.5rem;
    }
    
    .dashboard-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .alert-system-header {
            padding: 1.5rem 1rem;
        }
        
        .alert-critical, .alert-high, .alert-medium, .alert-low {
            padding: 1rem;
            margin: 0.8rem 0;
        }
        
        .rule-card {
            padding: 1rem;
        }
        
        .dashboard-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        
        .dashboard-metric {
            padding: 1rem;
        }
        
        .dashboard-value {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 480px) {
        .alert-status {
            font-size: 0.75rem;
            padding: 0.3rem 0.8rem;
        }
        
        .dashboard-grid {
            grid-template-columns: 1fr 1fr;
        }
        
        .dashboard-value {
            font-size: 1.8rem;
        }
    }
    
    /* Emergency protocols */
    .emergency-panel {
        background: linear-gradient(45deg, var(--police-red) 0%, #b91c1c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 20px rgba(220, 38, 38, 0.4);
        border: 2px solid white;
    }
    
    .emergency-panel h3 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Classification banner */
    .classification-banner {
        background: var(--police-red);
        color: white;
        text-align: center;
        padding: 0.5rem;
        font-weight: bold;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Security classification banner
    st.markdown("""
    <div class="classification-banner">
        🔒 CLASSIFIED - LAW ENFORCEMENT ALERT SYSTEM 🔒
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced alert system header
    st.markdown("""
    <div class="alert-system-header">
        <h1>🚨 POLICE ALERT MANAGEMENT SYSTEM</h1>
        <p>Advanced threat detection and response coordination for law enforcement</p>
        <div style="margin-top: 1rem; font-size: 1.1rem;">
            <strong>⚡ REAL-TIME MONITORING ACTIVE ⚡</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize alert manager
    if 'alert_manager' not in st.session_state:
        st.session_state.alert_manager = AlertManager()
    
    alert_manager = st.session_state.alert_manager
    
    # Sidebar for alert configuration
    with st.sidebar:
        st.header("🔧 Alert Configuration")
        
        # Quick actions
        st.subheader("Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh"):
                st.rerun()
        with col2:
            if st.button("🔕 Silence All"):
                alert_manager.silence_all_alerts()
                st.success("All alerts silenced!")
        
        # Alert rules management
        st.subheader("➕ Create Alert Rule")
        with st.expander("New Alert Rule"):
            rule_name = st.text_input("Rule Name")
            rule_type = st.selectbox(
                "Alert Type",
                ["Mention Spike", "Sentiment Drop", "Engagement Drop", "Keyword Alert", "Custom Metric"]
            )
            
            platform = st.multiselect(
                "Platforms",
                ["Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok"],
                default=["Twitter"]
            )
            
            threshold = st.number_input("Threshold Value", value=100)
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            
            notifications = st.multiselect(
                "Notifications",
                ["Email", "Slack", "SMS", "In-App"],
                default=["In-App"]
            )
            
            if st.button("Create Rule"):
                rule = AlertRule(
                    name=rule_name,
                    type=rule_type,
                    platforms=platform,
                    threshold=threshold,
                    severity=severity,
                    notifications=notifications
                )
                alert_manager.add_rule(rule)
                st.success(f"Alert rule '{rule_name}' created!")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Active Alerts", "📋 Alert Rules", "📊 Analytics", "⚙️ Settings"])
    
    with tab1:
        # Alert dashboard
        display_alert_dashboard(alert_manager)
        
        # Active alerts list
        st.subheader("Active Alerts")
        active_alerts = alert_manager.get_active_alerts()
        
        if not active_alerts:
            st.success("✅ No active alerts - All systems normal!")
        else:
            for alert in active_alerts:
                display_alert_card(alert, alert_manager)
    
    with tab2:
        # Alert rules management
        st.subheader("Alert Rules Configuration")
        
        rules = alert_manager.get_all_rules()
        
        if not rules:
            st.info("No alert rules configured. Create your first rule in the sidebar.")
        else:
            for rule in rules:
                display_rule_card(rule, alert_manager)
    
    with tab3:
        # Alert analytics
        display_alert_analytics(alert_manager)
    
    with tab4:
        # Alert settings
        display_alert_settings(alert_manager)

def display_alert_dashboard(alert_manager):
    """Display alert dashboard with key metrics"""
    # Get alert statistics
    stats = alert_manager.get_alert_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Active Alerts",
            stats['active_alerts'],
            delta=stats['new_alerts_today']
        )
    
    with col2:
        st.metric(
            "Critical Alerts",
            stats['critical_alerts'],
            delta=stats['critical_change']
        )
    
    with col3:
        st.metric(
            "Avg Response Time",
            f"{stats['avg_response_time']:.1f}min",
            delta=f"{stats['response_time_change']:+.1f}min"
        )
    
    with col4:
        st.metric(
            "Resolution Rate",
            f"{stats['resolution_rate']:.1%}",
            delta=f"{stats['resolution_change']:+.1%}"
        )
    
    # Alert trend chart
    st.subheader("Alert Trends (Last 24 Hours)")
    trend_chart = create_alert_trend_chart(alert_manager)
    st.plotly_chart(trend_chart, use_container_width=True)

def display_alert_card(alert, alert_manager):
    """Display individual alert card"""
    severity_class = f"alert-{alert['severity'].lower()}"
    status_class = f"status-{alert['status'].lower()}"
    
    with st.container():
        st.markdown(f"""
        <div class="{severity_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">{alert['title']}</h4>
                    <span class="alert-status {status_class}">{alert['status'].upper()}</span>
                </div>
                <div style="text-align: right;">
                    <div><strong>{alert['severity']}</strong></div>
                    <div style="font-size: 0.8rem;">{alert['timestamp'].strftime('%H:%M:%S')}</div>
                </div>
            </div>
            <div style="margin: 0.5rem 0;">
                <strong>Platform:</strong> {alert['platform']} | 
                <strong>Metric:</strong> {alert['metric']} | 
                <strong>Value:</strong> {alert['current_value']} (Threshold: {alert['threshold']})
            </div>
            <div style="margin: 0.5rem 0;">
                {alert['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Alert actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button(f"✅ Resolve", key=f"resolve_{alert['id']}"):
                alert_manager.resolve_alert(alert['id'])
                st.success("Alert resolved!")
                st.rerun()
        
        with col2:
            if st.button(f"🔕 Snooze", key=f"snooze_{alert['id']}"):
                alert_manager.snooze_alert(alert['id'], hours=1)
                st.info("Alert snoozed for 1 hour")
                st.rerun()
        
        with col3:
            if st.button(f"📧 Escalate", key=f"escalate_{alert['id']}"):
                alert_manager.escalate_alert(alert['id'])
                st.warning("Alert escalated!")
        
        with col4:
            if st.button(f"👁️ Details", key=f"details_{alert['id']}"):
                display_alert_details(alert)

def display_rule_card(rule, alert_manager):
    """Display alert rule card"""
    with st.container():
        st.markdown(f"""
        <div class="rule-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">{rule['name']}</h4>
                    <div><strong>Type:</strong> {rule['type']} | <strong>Severity:</strong> {rule['severity']}</div>
                </div>
                <div style="text-align: right;">
                    <div>{'🟢 Active' if rule['enabled'] else '🔴 Disabled'}</div>
                    <div style="font-size: 0.8rem;">Triggered: {rule['trigger_count']} times</div>
                </div>
            </div>
            <div style="margin: 0.5rem 0;">
                <strong>Platforms:</strong> {', '.join(rule['platforms'])} | 
                <strong>Threshold:</strong> {rule['threshold']} | 
                <strong>Notifications:</strong> {', '.join(rule['notifications'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Rule actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if rule['enabled']:
                if st.button(f"⏸️ Disable", key=f"disable_{rule['id']}"):
                    alert_manager.disable_rule(rule['id'])
                    st.info("Rule disabled")
                    st.rerun()
            else:
                if st.button(f"▶️ Enable", key=f"enable_{rule['id']}"):
                    alert_manager.enable_rule(rule['id'])
                    st.success("Rule enabled")
                    st.rerun()
        
        with col2:
            if st.button(f"✏️ Edit", key=f"edit_{rule['id']}"):
                edit_rule_dialog(rule, alert_manager)
        
        with col3:
            if st.button(f"🧪 Test", key=f"test_{rule['id']}"):
                alert_manager.test_rule(rule['id'])
                st.info("Test alert generated")
        
        with col4:
            if st.button(f"🗑️ Delete", key=f"delete_{rule['id']}"):
                alert_manager.delete_rule(rule['id'])
                st.success("Rule deleted")
                st.rerun()

def display_alert_analytics(alert_manager):
    """Display alert analytics"""
    st.subheader("Alert Analytics")
    
    # Alert frequency by type
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Alerts by Type")
        type_chart = create_alert_type_chart(alert_manager)
        st.plotly_chart(type_chart, use_container_width=True)
    
    with col2:
        st.subheader("Alerts by Severity")
        severity_chart = create_alert_severity_chart(alert_manager)
        st.plotly_chart(severity_chart, use_container_width=True)
    
    # Response time analysis
    st.subheader("Response Time Analysis")
    response_chart = create_response_time_chart(alert_manager)
    st.plotly_chart(response_chart, use_container_width=True)
    
    # Alert history table
    st.subheader("Recent Alert History")
    history = alert_manager.get_alert_history(limit=50)
    st.dataframe(history, use_container_width=True)

def display_alert_settings(alert_manager):
    """Display alert system settings"""
    st.subheader("Alert System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Notification Settings")
        
        # Email settings
        st.checkbox("Enable Email Notifications", value=True)
        st.text_input("Email Recipients", value="admin@company.com")
        
        # Slack settings
        st.checkbox("Enable Slack Notifications", value=True)
        st.text_input("Slack Webhook URL", type="password")
        
        # SMS settings
        st.checkbox("Enable SMS Notifications", value=False)
        st.text_input("SMS Recipients", value="+1234567890")
    
    with col2:
        st.subheader("General Settings")
        
        # Auto-resolve settings
        st.checkbox("Auto-resolve alerts", value=False)
        st.number_input("Auto-resolve after (hours)", value=24, min_value=1)
        
        # Escalation settings
        st.checkbox("Enable escalation", value=True)
        st.number_input("Escalate after (minutes)", value=60, min_value=5)
        
        # Rate limiting
        st.checkbox("Enable rate limiting", value=True)
        st.number_input("Max alerts per hour", value=100, min_value=1)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

def create_alert_trend_chart(alert_manager):
    """Create alert trend chart"""
    # Generate sample trend data
    hours = list(range(24))
    alerts = [alert_manager.get_alerts_by_hour(h) for h in hours]
    
    fig = px.line(
        x=hours,
        y=alerts,
        title="Alert Volume by Hour",
        labels={'x': 'Hour', 'y': 'Number of Alerts'}
    )
    fig.update_layout(height=300)
    return fig

def create_alert_type_chart(alert_manager):
    """Create alert type distribution chart"""
    type_data = alert_manager.get_alert_type_distribution()
    
    fig = px.pie(
        values=list(type_data.values()),
        names=list(type_data.keys()),
        title="Alert Distribution by Type"
    )
    fig.update_layout(height=300)
    return fig

def create_alert_severity_chart(alert_manager):
    """Create alert severity chart"""
    severity_data = alert_manager.get_alert_severity_distribution()
    
    colors = {
        'Critical': '#f44336',
        'High': '#ff9800',
        'Medium': '#9c27b0',
        'Low': '#4caf50'
    }
    
    fig = px.bar(
        x=list(severity_data.keys()),
        y=list(severity_data.values()),
        title="Alert Distribution by Severity",
        color=list(severity_data.keys()),
        color_discrete_map=colors
    )
    fig.update_layout(height=300, showlegend=False)
    return fig

def create_response_time_chart(alert_manager):
    """Create response time analysis chart"""
    response_data = alert_manager.get_response_time_data()
    
    fig = px.histogram(
        x=response_data,
        title="Alert Response Time Distribution",
        labels={'x': 'Response Time (minutes)', 'y': 'Number of Alerts'}
    )
    fig.update_layout(height=300)
    return fig

def display_alert_details(alert):
    """Display detailed alert information"""
    with st.expander(f"Alert Details - {alert['title']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Alert Information:**")
            st.write(f"ID: {alert['id']}")
            st.write(f"Metric: {alert.get('metric', 'N/A')}")
            st.write(f"Platform: {alert['platform']}")
            st.write(f"Severity: {alert['severity']}")
            st.write(f"Status: {alert['status']}")
        
        with col2:
            st.write("**Metrics:**")
            st.write(f"Current Value: {alert['current_value']}")
            st.write(f"Threshold: {alert['threshold']}")
            st.write(f"Percentage Change: {alert.get('change_percent', 'N/A')}")
            st.write(f"Duration: {alert.get('duration', 'N/A')}")
        
        st.write("**Description:**")
        st.write(alert['description'])
        
        st.write("**Timeline:**")
        timeline = alert.get('timeline', [])
        if timeline:
            for event in timeline:
                if isinstance(event, dict):
                    timestamp = event.get('timestamp', 'Unknown time')
                    event_desc = event.get('event', 'Unknown event')
                    st.write(f"• {timestamp}: {event_desc}")
                else:
                    st.write(f"• {event}")
        else:
            st.write("• No timeline events available")
        
        # Additional alert actions
        st.write("**Additional Information:**")
        st.write(f"Rule ID: {alert.get('rule_id', 'N/A')}")
        st.write(f"Timestamp: {alert.get('timestamp', 'N/A')}")
        if alert.get('escalated'):
            st.warning("⚠️ This alert has been escalated")
        if alert.get('snoozed_until'):
            st.info(f"😴 Snoozed until: {alert.get('snoozed_until')}")

def edit_rule_dialog(rule, alert_manager):
    """Edit rule dialog"""
    st.info(f"Editing rule: {rule['name']}")
    # Implementation would show edit form

if __name__ == "__main__":
    main()
