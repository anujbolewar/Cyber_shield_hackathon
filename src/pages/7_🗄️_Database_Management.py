#!/usr/bin/env python3
"""
🗄️ POLICE AI MONITOR - DATABASE MANAGEMENT
Comprehensive database connectivity and management interface
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

# Import the existing database manager
try:
    from utils.database_manager import PoliceMonitoringDB
    DB_MANAGER_AVAILABLE = True
except ImportError:
    st.error("Database manager not available. Please check utils/database_manager.py")
    DB_MANAGER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Database Management - Police AI Monitor",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Police Theme CSS
st.markdown("""
<style>
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
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    .database-header {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .database-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--police-accent) 0%, var(--police-red) 50%, var(--police-accent) 100%);
    }
    
    .database-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .connection-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.5rem 0;
        border: 2px solid;
    }
    
    .status-connected {
        background: rgba(22, 163, 74, 0.1);
        border-color: var(--police-green);
        color: var(--police-green);
    }
    
    .status-disconnected {
        background: rgba(220, 38, 38, 0.1);
        border-color: var(--police-red);
        color: var(--police-red);
    }
    
    .status-testing {
        background: rgba(251, 191, 36, 0.1);
        border-color: var(--police-accent);
        color: #d97706;
    }
    
    .metric-card {
        background: linear-gradient(135deg, white 0%, var(--police-light-gray) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid var(--police-blue);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);
    }
    
    .table-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .query-editor {
        background: #1e293b;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #e2e8f0;
    }
    
    .backup-item {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .backup-item:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .security-warning {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border: 2px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #dc2626;
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(22, 163, 74, 0.05) 100%);
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #16a34a;
    }
</style>
""", unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('user_authenticated', False):
        st.markdown("""
        <div class="security-warning">
            <h3>🔒 AUTHENTICATION REQUIRED</h3>
            <p>Please authenticate through the main application to access database management.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

def initialize_database_connection():
    """Initialize database connection"""
    if 'db_manager' not in st.session_state:
        if DB_MANAGER_AVAILABLE:
            try:
                st.session_state.db_manager = PoliceMonitoringDB("police_monitoring.db")
                st.session_state.db_connected = True
                st.session_state.db_status = "Connected"
                st.session_state.db_error = None
            except Exception as e:
                st.session_state.db_connected = False
                st.session_state.db_status = "Connection Failed"
                st.session_state.db_error = str(e)
        else:
            st.session_state.db_connected = False
            st.session_state.db_status = "Manager Unavailable"
            st.session_state.db_error = "Database manager not imported"

def display_database_header():
    """Display database management header"""
    st.markdown("""
    <div class="database-header">
        <div class="database-badge">
            🗄️ DATABASE MANAGEMENT CENTER
        </div>
        <h1>🔗 Police AI Monitor Database System</h1>
        <p>Comprehensive database connectivity, monitoring, and management interface</p>
    </div>
    """, unsafe_allow_html=True)

def display_connection_status():
    """Display current database connection status"""
    status = st.session_state.get('db_status', 'Unknown')
    connected = st.session_state.get('db_connected', False)
    error = st.session_state.get('db_error')
    
    if connected:
        status_class = "status-connected"
        status_icon = "🟢"
    else:
        status_class = "status-disconnected"
        status_icon = "🔴"
    
    st.markdown(f"""
    <div class="connection-status {status_class}">
        {status_icon} Database Status: {status}
    </div>
    """, unsafe_allow_html=True)
    
    if error:
        st.error(f"Database Error: {error}")

def display_database_statistics():
    """Display database statistics and metrics"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Statistics unavailable.")
        return
    
    try:
        db_manager = st.session_state.db_manager
        stats = db_manager.get_database_statistics()
        
        st.subheader("📊 Database Statistics")
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📝 Monitored Content</h3>
                <h2>{:,}</h2>
                <p>Total items tracked</p>
            </div>
            """.format(stats.get('monitored_content_count', 0)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🚨 Active Alerts</h3>
                <h2>{:,}</h2>
                <p>Alerts generated</p>
            </div>
            """.format(stats.get('alerts_count', 0)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>🔬 Investigations</h3>
                <h2>{:,}</h2>
                <p>Cases created</p>
            </div>
            """.format(stats.get('investigations_count', 0)), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>🔑 Keywords</h3>
                <h2>{:,}</h2>
                <p>Monitoring terms</p>
            </div>
            """.format(stats.get('keywords_count', 0)), unsafe_allow_html=True)
        
        # Recent activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📈 Last 24 Hours</h3>
                <p><strong>Content:</strong> {:,} items</p>
                <p><strong>Alerts:</strong> {:,} generated</p>
            </div>
            """.format(
                stats.get('content_last_24h', 0),
                stats.get('alerts_last_24h', 0)
            ), unsafe_allow_html=True)
        
        with col2:
            # Database size
            size_bytes = stats.get('database_size_bytes', 0)
            size_mb = size_bytes / (1024 * 1024) if size_bytes else 0
            
            st.markdown("""
            <div class="metric-card">
                <h3>💾 Database Size</h3>
                <p><strong>Size:</strong> {:.2f} MB</p>
                <p><strong>Users:</strong> {:,}</p>
            </div>
            """.format(size_mb, stats.get('users_count', 0)), unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading database statistics: {str(e)}")

def display_table_browser():
    """Display table browser and data viewer"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Table browser unavailable.")
        return
    
    st.subheader("🗃️ Table Browser")
    
    # Table selection
    tables = {
        "monitored_content": "📱 Monitored Content",
        "alerts": "🚨 Alerts",
        "investigations": "🔬 Investigations", 
        "keywords": "🔑 Keywords",
        "users": "👥 Users",
        "api_logs": "📋 API Logs",
        "audit_trail": "📜 Audit Trail"
    }
    
    selected_table = st.selectbox(
        "Select Table", 
        list(tables.keys()),
        format_func=lambda x: tables[x]
    )
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        limit = st.number_input("Rows to display", min_value=10, max_value=1000, value=50)
    
    with col2:
        offset = st.number_input("Starting from row", min_value=0, value=0)
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    try:
        db_manager = st.session_state.db_manager
        
        # Get data based on selected table
        if selected_table == "monitored_content":
            data = db_manager.get_monitored_content(limit=limit, offset=offset)
        elif selected_table == "alerts":
            data = db_manager.get_alerts(limit=limit)
        elif selected_table == "investigations":
            data = db_manager.get_investigations(limit=limit)
        elif selected_table == "keywords":
            data = db_manager.get_keywords()
        elif selected_table == "users":
            data = db_manager.get_users()
        elif selected_table == "api_logs":
            data = db_manager.get_api_logs(limit=limit)
        else:
            # For audit_trail, use direct query
            with db_manager.get_connection() as conn:
                query = f"SELECT * FROM {selected_table} ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                data = pd.read_sql_query(query, conn, params=[limit, offset]).to_dict('records')
        
        if data:
            df = pd.DataFrame(data)
            
            st.markdown(f"""
            <div class="table-container">
                <h4>📊 {tables[selected_table]} ({len(data)} rows)</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display data with improved formatting
            display_df = df.copy()
            
            # Format timestamp columns
            for col in display_df.columns:
                if 'timestamp' in col.lower() or 'created_at' in col.lower() or 'updated_at' in col.lower():
                    if display_df[col].dtype == 'object':
                        try:
                            display_df[col] = pd.to_datetime(display_df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            pass
            
            # Truncate long text columns
            for col in display_df.columns:
                if display_df[col].dtype == 'object':
                    display_df[col] = display_df[col].astype(str).apply(
                        lambda x: x[:100] + '...' if len(x) > 100 else x
                    )
            
            st.dataframe(display_df, use_container_width=True)
            
            # Export options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Export CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
            
            with col2:
                if st.button("📥 Export JSON"):
                    json_data = df.to_json(orient='records', indent=2)
                    st.download_button(
                        "Download JSON",
                        json_data,
                        f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        "application/json"
                    )
            
        else:
            st.info(f"No data found in {tables[selected_table]} table.")
            
    except Exception as e:
        st.error(f"Error loading table data: {str(e)}")

def display_query_interface():
    """Display SQL query interface for advanced users"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Query interface unavailable.")
        return
    
    st.subheader("🔍 Advanced Query Interface")
    
    # Security warning
    st.markdown("""
    <div class="security-warning">
        <h4>⚠️ SECURITY WARNING</h4>
        <p>This interface allows direct database queries. Only authorized personnel should use this feature.
        Destructive operations are disabled for security.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pre-defined queries
    predefined_queries = {
        "High Risk Content": """
            SELECT content, author, platform, risk_score, threat_level, timestamp
            FROM monitored_content 
            WHERE risk_score >= 70 
            ORDER BY risk_score DESC 
            LIMIT 20
        """,
        
        "Recent Alerts": """
            SELECT a.alert_id, a.type, a.severity, a.message, a.status, a.timestamp,
                   mc.platform, mc.author
            FROM alerts a
            LEFT JOIN monitored_content mc ON a.content_id = mc.id
            WHERE a.timestamp >= datetime('now', '-7 days')
            ORDER BY a.timestamp DESC
        """,
        
        "Active Investigations": """
            SELECT case_id, title, status, priority, lead_officer, created_at
            FROM investigations 
            WHERE status IN ('OPEN', 'ACTIVE', 'UNDER_REVIEW')
            ORDER BY created_at DESC
        """,
        
        "Platform Statistics": """
            SELECT platform, 
                   COUNT(*) as total_content,
                   AVG(risk_score) as avg_risk_score,
                   COUNT(CASE WHEN threat_level = 'HIGH' THEN 1 END) as high_threats
            FROM monitored_content 
            WHERE created_at >= datetime('now', '-30 days')
            GROUP BY platform
            ORDER BY total_content DESC
        """,
        
        "Keyword Performance": """
            SELECT k.term, k.category, k.risk_level,
                   COUNT(mc.id) as matches
            FROM keywords k
            LEFT JOIN monitored_content mc ON mc.content LIKE '%' || k.term || '%'
            WHERE k.is_active = 1
            GROUP BY k.term, k.category, k.risk_level
            HAVING matches > 0
            ORDER BY matches DESC
            LIMIT 15
        """
    }
    
    # Query selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_query = st.selectbox(
            "Pre-defined Queries",
            ["Custom Query"] + list(predefined_queries.keys())
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        execute_button = st.button("▶️ Execute Query", type="primary")
    
    # Query editor
    if selected_query == "Custom Query":
        query = st.text_area(
            "SQL Query",
            height=200,
            placeholder="Enter your SQL query here...",
            help="Only SELECT queries are allowed for security reasons."
        )
    else:
        query = st.text_area(
            "SQL Query",
            value=predefined_queries[selected_query].strip(),
            height=200
        )
    
    # Execute query
    if execute_button and query.strip():
        try:
            # Security check - only allow SELECT queries
            query_upper = query.upper().strip()
            if not query_upper.startswith('SELECT'):
                st.error("🚫 Only SELECT queries are allowed for security reasons.")
                return
            
            # Additional security checks
            forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
            for keyword in forbidden_keywords:
                if keyword in query_upper:
                    st.error(f"🚫 Forbidden keyword detected: {keyword}")
                    return
            
            db_manager = st.session_state.db_manager
            
            with db_manager.get_connection() as conn:
                start_time = datetime.now()
                df = pd.read_sql_query(query, conn)
                execution_time = (datetime.now() - start_time).total_seconds()
            
            st.markdown("""
            <div class="success-message">
                <h4>✅ Query Executed Successfully</h4>
                <p><strong>Execution Time:</strong> {:.3f} seconds</p>
                <p><strong>Rows Returned:</strong> {:,}</p>
            </div>
            """.format(execution_time, len(df)), unsafe_allow_html=True)
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # Export results
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download as CSV",
                        csv,
                        f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
                
                with col2:
                    json_data = df.to_json(orient='records', indent=2)
                    st.download_button(
                        "📥 Download as JSON",
                        json_data,
                        f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        "application/json"
                    )
            else:
                st.info("Query executed successfully but returned no results.")
                
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")

def display_backup_management():
    """Display backup and restore interface"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Backup management unavailable.")
        return
    
    st.subheader("💾 Backup & Restore Management")
    
    db_manager = st.session_state.db_manager
    
    # Create backup section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        backup_name = st.text_input(
            "Backup Name (optional)",
            placeholder="Leave empty for auto-generated name"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Create Backup", type="primary"):
            try:
                backup_path = db_manager.create_backup(backup_name if backup_name else None)
                if backup_path:
                    st.success(f"✅ Backup created successfully: {backup_path}")
                else:
                    st.error("❌ Backup creation failed")
            except Exception as e:
                st.error(f"Backup error: {str(e)}")
    
    # List existing backups
    try:
        backups = db_manager.list_backups()
        
        if backups:
            st.markdown("### 📋 Available Backups")
            
            for backup in backups:
                with st.container():
                    st.markdown(f"""
                    <div class="backup-item">
                        <div>
                            <strong>{backup['filename']}</strong><br>
                            <small>Created: {backup['created_at'][:19]} | Size: {backup['size_bytes']:,} bytes</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        if st.button(f"📥 Download", key=f"download_{backup['filename']}"):
                            with open(backup['filepath'], 'rb') as f:
                                st.download_button(
                                    "Download Backup",
                                    f.read(),
                                    backup['filename'],
                                    "application/octet-stream"
                                )
                    
                    with col2:
                        if st.button(f"🔄 Restore", key=f"restore_{backup['filename']}", type="secondary"):
                            if st.button(f"⚠️ Confirm Restore", key=f"confirm_{backup['filename']}"):
                                try:
                                    success = db_manager.restore_backup(backup['filepath'])
                                    if success:
                                        st.success(f"✅ Database restored from {backup['filename']}")
                                        st.rerun()
                                    else:
                                        st.error("❌ Restore failed")
                                except Exception as e:
                                    st.error(f"Restore error: {str(e)}")
                    
                    st.markdown("---")
        else:
            st.info("No backups available")
            
    except Exception as e:
        st.error(f"Error listing backups: {str(e)}")
    
    # Cleanup section
    st.markdown("### 🧹 Backup Cleanup")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        cleanup_days = st.number_input(
            "Delete backups older than (days)",
            min_value=1,
            max_value=365,
            value=30
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Cleanup Old Backups"):
            try:
                deleted_count = db_manager.cleanup_old_backups(cleanup_days)
                st.info(f"🧹 Cleaned up {deleted_count} old backup(s)")
            except Exception as e:
                st.error(f"Cleanup error: {str(e)}")

def display_analytics_dashboard():
    """Display database analytics and visualizations"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Analytics unavailable.")
        return
    
    st.subheader("📈 Database Analytics Dashboard")
    
    try:
        db_manager = st.session_state.db_manager
        analytics = db_manager.get_threat_analytics(days_back=30)
        
        if not analytics:
            st.info("No analytics data available")
            return
        
        # Content statistics overview
        content_stats = analytics.get('content_statistics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Content",
                f"{content_stats.get('total_content', 0):,}",
                delta=None
            )
        
        with col2:
            avg_risk = content_stats.get('avg_risk_score', 0)
            st.metric(
                "Avg Risk Score",
                f"{avg_risk:.1f}",
                delta=f"{avg_risk - 50:.1f}" if avg_risk else None
            )
        
        with col3:
            st.metric(
                "Critical Threats",
                f"{content_stats.get('critical_threats', 0):,}",
                delta=None
            )
        
        with col4:
            st.metric(
                "Flagged Content",
                f"{content_stats.get('flagged_content', 0):,}",
                delta=None
            )
        
        # Platform distribution chart
        platform_data = analytics.get('platform_distribution', [])
        if platform_data:
            st.markdown("### 📱 Content by Platform")
            
            platforms_df = pd.DataFrame(platform_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Platform count pie chart
                fig_pie = px.pie(
                    platforms_df,
                    values='count',
                    names='platform',
                    title="Content Distribution by Platform",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Platform risk bar chart
                fig_bar = px.bar(
                    platforms_df,
                    x='platform',
                    y='avg_risk',
                    title="Average Risk Score by Platform",
                    color='avg_risk',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Daily trends
        daily_trends = analytics.get('daily_trends', [])
        if daily_trends:
            st.markdown("### 📅 Daily Threat Trends")
            
            trends_df = pd.DataFrame(daily_trends)
            trends_df['date'] = pd.to_datetime(trends_df['date'])
            
            # Multi-line chart for trends
            fig_trends = go.Figure()
            
            fig_trends.add_trace(go.Scatter(
                x=trends_df['date'],
                y=trends_df['content_count'],
                mode='lines+markers',
                name='Content Count',
                yaxis='y'
            ))
            
            fig_trends.add_trace(go.Scatter(
                x=trends_df['date'],
                y=trends_df['avg_risk'],
                mode='lines+markers',
                name='Avg Risk Score',
                yaxis='y2'
            ))
            
            fig_trends.update_layout(
                title="Daily Content and Risk Trends",
                xaxis_title="Date",
                yaxis=dict(title="Content Count", side="left"),
                yaxis2=dict(title="Average Risk Score", side="right", overlaying="y"),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)
        
        # Alert statistics
        alert_stats = analytics.get('alert_statistics', {})
        if alert_stats:
            st.markdown("### 🚨 Alert Statistics")
            
            # Create alert summary table
            alert_summary = []
            for status, severities in alert_stats.items():
                for severity, count in severities.items():
                    alert_summary.append({
                        'Status': status,
                        'Severity': severity,
                        'Count': count
                    })
            
            if alert_summary:
                alert_df = pd.DataFrame(alert_summary)
                
                # Alert heatmap
                pivot_df = alert_df.pivot(index='Status', columns='Severity', values='Count').fillna(0)
                
                fig_heatmap = px.imshow(
                    pivot_df,
                    title="Alert Status vs Severity Heatmap",
                    color_continuous_scale='Reds',
                    aspect='auto'
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Top keywords
        top_keywords = analytics.get('top_keywords', [])
        if top_keywords:
            st.markdown("### 🔑 Top Performing Keywords")
            
            keywords_df = pd.DataFrame(top_keywords)
            
            fig_keywords = px.bar(
                keywords_df.head(10),
                x='matches',
                y='term',
                orientation='h',
                title="Keywords by Match Count",
                color='category',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig_keywords.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_keywords, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error generating analytics: {str(e)}")

def display_maintenance_tools():
    """Display database maintenance and optimization tools"""
    if not st.session_state.get('db_connected', False):
        st.warning("⚠️ Database not connected. Maintenance tools unavailable.")
        return
    
    st.subheader("🔧 Database Maintenance")
    
    db_manager = st.session_state.db_manager
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🗄️ Database Optimization")
        
        if st.button("🔄 Vacuum Database"):
            try:
                with db_manager.get_connection() as conn:
                    conn.execute("VACUUM")
                st.success("✅ Database vacuum completed")
            except Exception as e:
                st.error(f"Vacuum failed: {str(e)}")
        
        if st.button("📊 Analyze Tables"):
            try:
                with db_manager.get_connection() as conn:
                    conn.execute("ANALYZE")
                st.success("✅ Table analysis completed")
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
        
        if st.button("🔍 Integrity Check"):
            try:
                with db_manager.get_connection() as conn:
                    result = conn.execute("PRAGMA integrity_check").fetchone()
                    if result[0] == 'ok':
                        st.success("✅ Database integrity check passed")
                    else:
                        st.error(f"❌ Integrity check failed: {result[0]}")
            except Exception as e:
                st.error(f"Integrity check failed: {str(e)}")
    
    with col2:
        st.markdown("#### 📋 Information")
        
        try:
            with db_manager.get_connection() as conn:
                # Get database info
                page_count = conn.execute("PRAGMA page_count").fetchone()[0]
                page_size = conn.execute("PRAGMA page_size").fetchone()[0]
                db_size_mb = (page_count * page_size) / (1024 * 1024)
                
                journal_mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
                cache_size = conn.execute("PRAGMA cache_size").fetchone()[0]
                
                st.info(f"""
                **Database Information:**
                - Size: {db_size_mb:.2f} MB
                - Pages: {page_count:,}
                - Page Size: {page_size:,} bytes
                - Journal Mode: {journal_mode}
                - Cache Size: {cache_size:,} pages
                """)
                
        except Exception as e:
            st.error(f"Error getting database info: {str(e)}")

def main():
    """Main function for database management page"""
    check_authentication()
    initialize_database_connection()
    
    display_database_header()
    display_connection_status()
    
    if not st.session_state.get('db_connected', False):
        st.markdown("""
        <div class="security-warning">
            <h3>⚠️ DATABASE CONNECTION REQUIRED</h3>
            <p>Database connection failed. Please check:</p>
            <ul>
                <li>Database file permissions</li>
                <li>Database manager configuration</li>
                <li>System resources availability</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🗄️ Database Operations")
        
        operation = st.selectbox(
            "Select Operation",
            [
                "📊 Statistics Overview",
                "🗃️ Table Browser", 
                "🔍 Query Interface",
                "📈 Analytics Dashboard",
                "💾 Backup Management",
                "🔧 Maintenance Tools"
            ]
        )
        
        # Connection info
        st.markdown("---")
        st.markdown("### 🔗 Connection Info")
        
        db_path = getattr(st.session_state.get('db_manager'), 'db_path', 'Unknown')
        st.info(f"**Database:** {db_path}")
        
        if st.button("🔄 Reconnect"):
            if 'db_manager' in st.session_state:
                del st.session_state.db_manager
            initialize_database_connection()
            st.rerun()
    
    # Main content based on selected operation
    if operation == "📊 Statistics Overview":
        display_database_statistics()
    
    elif operation == "🗃️ Table Browser":
        display_table_browser()
    
    elif operation == "🔍 Query Interface":
        display_query_interface()
    
    elif operation == "📈 Analytics Dashboard":
        display_analytics_dashboard()
    
    elif operation == "💾 Backup Management":
        display_backup_management()
    
    elif operation == "🔧 Maintenance Tools":
        display_maintenance_tools()

if __name__ == "__main__":
    main()
