#!/usr/bin/env python3
"""
⚖️ LEGAL EVIDENCE MANAGEMENT - STREAMLIT INTERFACE
Comprehensive legal evidence handling dashboard for police departments
Features: Evidence collection, verification, court formatting, expert testimony
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
import zipfile

# Add the utils directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

try:
    from legal_evidence_manager import LegalEvidenceManager, EvidenceType, LegalStatus
except ImportError:
    st.error("❌ Could not import Legal Evidence Manager modules. Please ensure all dependencies are installed.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Legal Evidence Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'evidence_manager' not in st.session_state:
        st.session_state.evidence_manager = None
    if 'current_case' not in st.session_state:
        st.session_state.current_case = ""
    if 'selected_evidence' not in st.session_state:
        st.session_state.selected_evidence = None
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

def get_evidence_theme_css(dark_mode=False):
    """Generate CSS based on theme mode for evidence manager"""
    if dark_mode:
        return """
<style>
    /* Dark Mode Theme for Legal Evidence Manager */
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --evidence-gold: #fbbf24;
        --evidence-blue: #3b82f6;
        --evidence-green: #22c55e;
        --evidence-red: #ef4444;
        --border-color: #475569;
    }
    
    .main .block-container {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Evidence header - Dark */
    .evidence-header {
        background: linear-gradient(90deg, #8B4513 0%, #2F4F4F 100%);
        color: var(--text-primary);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
    }
    
    /* Evidence cards - Dark */
    .evidence-card {
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
        background: linear-gradient(135deg, var(--evidence-blue) 0%, #1d4ed8 100%);
        color: white;
        border: 1px solid var(--evidence-blue);
    }
    
    /* Input fields - Dark */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-tertiary);
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
        background: var(--evidence-blue);
        color: white;
    }
    
    /* Expander - Dark */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    
    /* Status badges - Dark */
    .status-badge {
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-collected { background: var(--evidence-blue); color: white; }
    .status-verified { background: var(--evidence-green); color: white; }
    .status-court-ready { background: var(--evidence-gold); color: black; }
</style>
"""
    else:
        return """
<style>
    /* Light Mode Theme for Legal Evidence Manager */
    .evidence-header {
        background: linear-gradient(90deg, #8B4513 0%, #2F4F4F 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .evidence-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-badge {
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-collected { background: #3b82f6; color: white; }
    .status-verified { background: #22c55e; color: white; }
    .status-court-ready { background: #fbbf24; color: black; }
</style>
"""

def load_evidence_data(db_path: str) -> pd.DataFrame:
    """Load evidence data from database"""
    try:
        if not Path(db_path).exists():
            return pd.DataFrame()
        
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            evidence_id, case_number, evidence_type, source_platform,
            collected_by, collected_at, location_collected, description,
            legal_status, court_formatted, created_at
        FROM legal_evidence 
        ORDER BY created_at DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['collected_at'] = pd.to_datetime(df['collected_at'])
            df['created_at'] = pd.to_datetime(df['created_at'])
        
        return df
        
    except Exception as e:
        st.error(f"Error loading evidence data: {str(e)}")
        return pd.DataFrame()

def load_chain_of_custody(db_path: str, evidence_id: str) -> pd.DataFrame:
    """Load chain of custody data for specific evidence"""
    try:
        if not Path(db_path).exists():
            return pd.DataFrame()
        
        conn = sqlite3.connect(db_path)
        
        query = """
        SELECT 
            timestamp, officer_id, officer_name, action, 
            location, notes, system_hash
        FROM chain_of_custody 
        WHERE evidence_id = ?
        ORDER BY timestamp
        """
        
        df = pd.read_sql_query(query, conn, params=(evidence_id,))
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
        
    except Exception as e:
        st.error(f"Error loading chain of custody: {str(e)}")
        return pd.DataFrame()

def display_evidence_collection_form():
    """Display evidence collection form"""
    st.subheader("📋 Collect New Evidence")
    
    with st.form("evidence_collection_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            case_number = st.text_input(
                "Case Number*",
                placeholder="FIR_2025_001",
                help="Enter the FIR or case number"
            )
            
            evidence_type = st.selectbox(
                "Evidence Type*",
                options=[e.value for e in EvidenceType],
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            source_platform = st.text_input(
                "Source Platform",
                placeholder="Twitter, Facebook, WhatsApp, etc.",
                help="Platform where evidence was found"
            )
            
            collected_by = st.text_input(
                "Collected By*",
                placeholder="Officer ID or Name",
                help="Officer responsible for collection"
            )
        
        with col2:
            location_collected = st.text_input(
                "Collection Location*",
                placeholder="Mumbai Police Station",
                help="Physical location where evidence was collected"
            )
            
            description = st.text_area(
                "Evidence Description*",
                placeholder="Describe the evidence and its relevance to the case",
                help="Detailed description for legal documentation"
            )
            
            uploaded_files = st.file_uploader(
                "Upload Evidence Files",
                accept_multiple_files=True,
                help="Upload screenshots, documents, or other digital files"
            )
        
        # Source data input
        st.markdown("**Source Data (JSON format):**")
        source_data_text = st.text_area(
            "Source Data",
            placeholder='{"platform": "Twitter", "tweet_id": "123", "content": "Evidence content", "author": "username"}',
            help="Structured data about the evidence source"
        )
        
        # Submit button
        submitted = st.form_submit_button("🔒 Collect Evidence", type="primary")
        
        if submitted:
            # Validate required fields
            if not all([case_number, evidence_type, collected_by, location_collected, description]):
                st.error("❌ Please fill in all required fields marked with *")
                return
            
            try:
                # Parse source data
                if source_data_text.strip():
                    source_data = json.loads(source_data_text)
                else:
                    source_data = {
                        "platform": source_platform,
                        "description": description,
                        "collection_method": "manual_entry"
                    }
                
                # Save uploaded files temporarily
                file_paths = []
                if uploaded_files:
                    temp_dir = Path("temp_uploads")
                    temp_dir.mkdir(exist_ok=True)
                    
                    for uploaded_file in uploaded_files:
                        file_path = temp_dir / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        file_paths.append(str(file_path))
                
                # Collect evidence
                evidence_id = st.session_state.evidence_manager.collect_evidence(
                    case_number=case_number,
                    evidence_type=EvidenceType(evidence_type),
                    source_data=source_data,
                    collected_by=collected_by,
                    location=location_collected,
                    description=description,
                    file_paths=file_paths
                )
                
                if evidence_id:
                    st.success(f"✅ Evidence collected successfully! Evidence ID: {evidence_id}")
                    st.balloons()
                    
                    # Clean up temp files
                    for file_path in file_paths:
                        try:
                            Path(file_path).unlink()
                        except:
                            pass
                    
                    # Refresh the page
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Failed to collect evidence. Please check the logs.")
            
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON format in source data. Please check the syntax.")
            except Exception as e:
                st.error(f"❌ Error collecting evidence: {str(e)}")

def display_evidence_list(df: pd.DataFrame):
    """Display list of evidence with actions"""
    if df.empty:
        st.info("No evidence found. Collect some evidence to get started.")
        return
    
    st.subheader("📁 Evidence Inventory")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        case_filter = st.selectbox(
            "Filter by Case",
            options=["All"] + list(df['case_number'].unique()),
            key="case_filter"
        )
    
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All"] + list(df['legal_status'].unique()),
            key="status_filter"
        )
    
    with col3:
        type_filter = st.selectbox(
            "Filter by Type",
            options=["All"] + list(df['evidence_type'].unique()),
            key="type_filter"
        )
    
    with col4:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now().date() - timedelta(days=30), datetime.now().date()),
            key="date_filter"
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if case_filter != "All":
        filtered_df = filtered_df[filtered_df['case_number'] == case_filter]
    
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['legal_status'] == status_filter]
    
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['evidence_type'] == type_filter]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['collected_at'].dt.date >= start_date) &
            (filtered_df['collected_at'].dt.date <= end_date)
        ]
    
    # Display filtered results
    st.write(f"Showing {len(filtered_df)} of {len(df)} evidence items")
    
    # Evidence table with actions
    for idx, evidence in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"**Evidence ID:** `{evidence['evidence_id']}`")
                st.markdown(f"**Case:** {evidence['case_number']}")
                st.write(f"**Description:** {evidence['description'][:100]}...")
                st.caption(f"Collected: {evidence['collected_at'].strftime('%Y-%m-%d %H:%M')}")
            
            with col2:
                # Status badge
                status_colors = {
                    'collected': 'blue',
                    'verified': 'green',
                    'sealed': 'orange',
                    'submitted': 'purple'
                }
                status_color = status_colors.get(evidence['legal_status'], 'gray')
                st.markdown(f"**Status:** :{status_color}[{evidence['legal_status'].upper()}]")
                st.write(f"**Type:** {evidence['evidence_type'].replace('_', ' ').title()}")
                st.write(f"**Platform:** {evidence['source_platform'] or 'N/A'}")
            
            with col3:
                st.write(f"**Collected by:** {evidence['collected_by']}")
                st.write(f"**Location:** {evidence['location_collected']}")
                court_status = "✅ Yes" if evidence['court_formatted'] else "❌ No"
                st.write(f"**Court Ready:** {court_status}")
            
            with col4:
                # Action buttons
                if st.button(f"🔍 View Details", key=f"view_{evidence['evidence_id']}"):
                    st.session_state.selected_evidence = evidence['evidence_id']
                    st.rerun()
                
                if st.button(f"✅ Verify", key=f"verify_{evidence['evidence_id']}"):
                    verify_evidence(evidence['evidence_id'])
                
                if evidence['legal_status'] in ['collected', 'verified'] and not evidence['court_formatted']:
                    if st.button(f"⚖️ Format for Court", key=f"court_{evidence['evidence_id']}"):
                        format_for_court(evidence['evidence_id'])
            
            st.divider()

def verify_evidence(evidence_id: str):
    """Verify evidence integrity"""
    with st.spinner("Verifying evidence integrity..."):
        verification_results = st.session_state.evidence_manager.verify_evidence_integrity(evidence_id)
        
        if verification_results.get("error"):
            st.error(f"❌ Verification failed: {verification_results['error']}")
            return
        
        integrity_score = verification_results.get("integrity_score", 0)
        checks_passed = verification_results.get("checks_passed", 0)
        total_checks = verification_results.get("total_checks", 0)
        
        if integrity_score >= 0.8:
            st.success(f"✅ Evidence verified! Integrity score: {integrity_score:.2f} ({checks_passed}/{total_checks} checks passed)")
        else:
            st.warning(f"⚠️ Evidence integrity questionable. Score: {integrity_score:.2f} ({checks_passed}/{total_checks} checks passed)")
        
        # Show detailed results
        with st.expander("🔍 Detailed Verification Results"):
            for check, result in verification_results.get("details", {}).items():
                status = "✅" if result else "❌"
                st.write(f"{status} {check.replace('_', ' ').title()}: {'Passed' if result else 'Failed'}")

def format_for_court(evidence_id: str):
    """Format evidence for court submission"""
    st.subheader("⚖️ Format Evidence for Court")
    
    with st.form(f"court_format_{evidence_id}"):
        st.write(f"**Evidence ID:** {evidence_id}")
        
        court_name = st.text_input("Court Name*", placeholder="Sessions Court, Mumbai")
        judge_name = st.text_input("Judge Name", placeholder="Hon. Justice Name")
        prosecutor_name = st.text_input("Prosecutor Name*", placeholder="Public Prosecutor Name")
        prosecutor_id = st.text_input("Prosecutor ID", placeholder="Prosecutor identification")
        
        submitted = st.form_submit_button("📦 Create Court Package", type="primary")
        
        if submitted:
            if not court_name or not prosecutor_name:
                st.error("❌ Please fill in required court details")
                return
            
            court_details = {
                "court_name": court_name,
                "judge_name": judge_name,
                "prosecutor_name": prosecutor_name,
                "prosecutor_id": prosecutor_id
            }
            
            with st.spinner("Creating court submission package..."):
                package_path = st.session_state.evidence_manager.format_for_court(evidence_id, court_details)
                
                if package_path:
                    st.success("✅ Court package created successfully!")
                    
                    # Offer download
                    if Path(package_path).exists():
                        with open(package_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Download Court Package",
                                data=file.read(),
                                file_name=Path(package_path).name,
                                mime="application/zip"
                            )
                else:
                    st.error("❌ Failed to create court package")

def display_evidence_details(evidence_id: str):
    """Display detailed evidence information"""
    st.subheader(f"🔍 Evidence Details: {evidence_id}")
    
    # Load evidence data
    if not st.session_state.evidence_manager:
        st.error("Evidence manager not initialized")
        return
    
    db_path = st.session_state.evidence_manager.db_path
    
    # Get evidence metadata
    evidence_dir = st.session_state.evidence_manager.evidence_dir / evidence_id
    metadata_file = evidence_dir / "evidence_metadata.json"
    
    if not metadata_file.exists():
        st.error("Evidence metadata not found")
        return
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Display evidence information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Basic Information")
        st.write(f"**Evidence ID:** {metadata['evidence_id']}")
        st.write(f"**Case Number:** {metadata['case_number']}")
        st.write(f"**Type:** {metadata['evidence_type'].replace('_', ' ').title()}")
        st.write(f"**Source Platform:** {metadata.get('source_platform', 'N/A')}")
        st.write(f"**Collected By:** {metadata['collected_by']}")
        st.write(f"**Collection Time:** {metadata['collected_at']}")
        st.write(f"**Location:** {metadata['location_collected']}")
        st.write(f"**Status:** {metadata.get('legal_status', 'Unknown')}")
    
    with col2:
        st.markdown("### 🔐 Technical Details")
        st.write(f"**Original Hash:** `{metadata['original_hash'][:32]}...`")
        st.write(f"**Current Hash:** `{metadata['current_hash'][:32]}...`")
        st.write(f"**Digital Signature:** `{metadata['digital_signature'][:32]}...`")
        
        # Integrity check
        integrity_intact = metadata['original_hash'] == metadata['current_hash']
        integrity_status = "✅ INTACT" if integrity_intact else "❌ COMPROMISED"
        st.write(f"**Integrity:** {integrity_status}")
    
    # Description
    st.markdown("### 📝 Description")
    st.write(metadata['description'])
    
    # Source data
    with st.expander("📊 Source Data"):
        source_file = evidence_dir / "source_data.json"
        if source_file.exists():
            with open(source_file, 'r') as f:
                source_data = json.load(f)
            st.json(source_data)
        else:
            st.info("No source data available")
    
    # Chain of custody
    st.markdown("### 🔗 Chain of Custody")
    custody_df = load_chain_of_custody(db_path, evidence_id)
    
    if not custody_df.empty:
        st.dataframe(
            custody_df[['timestamp', 'officer_name', 'action', 'location', 'notes']],
            use_container_width=True
        )
    else:
        st.info("No chain of custody records found")
    
    # Actions
    st.markdown("### ⚡ Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("✅ Verify Integrity"):
            verify_evidence(evidence_id)
    
    with col2:
        if st.button("👨‍💼 Prepare Expert Testimony"):
            prepare_expert_testimony(evidence_id)
    
    with col3:
        if st.button("⚖️ Format for Court"):
            format_for_court(evidence_id)
    
    with col4:
        if st.button("📤 Export Evidence"):
            export_evidence(evidence_id)

def prepare_expert_testimony(evidence_id: str):
    """Prepare expert testimony for evidence"""
    st.subheader("👨‍💼 Prepare Expert Testimony")
    
    with st.form(f"expert_testimony_{evidence_id}"):
        expert_name = st.text_input("Expert Name*", value="Digital Forensics Expert")
        expert_credentials = st.text_area(
            "Expert Credentials*",
            value="Certified Digital Forensics Examiner, Ph.D. Computer Science"
        )
        
        submitted = st.form_submit_button("📋 Prepare Testimony", type="primary")
        
        if submitted:
            if not expert_name or not expert_credentials:
                st.error("❌ Please provide expert details")
                return
            
            expert_details = {
                "name": expert_name,
                "credentials": expert_credentials
            }
            
            with st.spinner("Preparing expert testimony..."):
                analysis = st.session_state.evidence_manager.prepare_expert_testimony(evidence_id, expert_details)
                
                if analysis.get("error"):
                    st.error(f"❌ Failed to prepare testimony: {analysis['error']}")
                else:
                    st.success("✅ Expert testimony prepared successfully!")
                    
                    with st.expander("📋 Testimony Summary"):
                        st.write(f"**Expert:** {analysis['expert_name']}")
                        st.write(f"**Confidence Level:** {analysis['confidence_level']}")
                        st.write(f"**Conclusions:** {analysis['conclusions']}")
                        st.write(f"**Methodology:** {analysis['methodology']}")

def export_evidence(evidence_id: str):
    """Export evidence package"""
    evidence_dir = st.session_state.evidence_manager.evidence_dir / evidence_id
    
    if not evidence_dir.exists():
        st.error("Evidence directory not found")
        return
    
    # Create export package
    export_path = evidence_dir / f"export_{evidence_id}.zip"
    
    with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in evidence_dir.rglob("*"):
            if file_path.is_file() and file_path != export_path:
                arcname = str(file_path.relative_to(evidence_dir))
                zipf.write(file_path, arcname)
    
    # Offer download
    with open(export_path, "rb") as file:
        st.download_button(
            label="⬇️ Download Evidence Package",
            data=file.read(),
            file_name=f"evidence_{evidence_id}.zip",
            mime="application/zip"
        )

def display_analytics_dashboard(df: pd.DataFrame):
    """Display analytics dashboard"""
    if df.empty:
        st.info("No data available for analytics")
        return
    
    st.subheader("📊 Evidence Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Evidence", len(df))
    
    with col2:
        court_ready = df['court_formatted'].sum()
        st.metric("Court Ready", court_ready)
    
    with col3:
        unique_cases = df['case_number'].nunique()
        st.metric("Active Cases", unique_cases)
    
    with col4:
        recent_count = len(df[df['created_at'] > datetime.now() - timedelta(days=7)])
        st.metric("This Week", recent_count)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Evidence by status
        status_counts = df['legal_status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Evidence by Legal Status"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Evidence by type
        type_counts = df['evidence_type'].value_counts()
        fig_type = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Evidence by Type"
        )
        fig_type.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Timeline
    if len(df) > 1:
        df_timeline = df.groupby(df['created_at'].dt.date).size().reset_index()
        df_timeline.columns = ['date', 'count']
        
        fig_timeline = px.line(
            df_timeline,
            x='date',
            y='count',
            title="Evidence Collection Timeline"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Apply theme CSS
    st.markdown(get_evidence_theme_css(False), unsafe_allow_html=True)
    
    # Header
    header_class = "evidence-header" if not st.session_state.dark_mode else "evidence-header"
    st.markdown(f"""
    <div class="{header_class}">
        <h1 style="color: white; margin: 0; display: flex; align-items: center;">
            ⚖️ Legal Evidence Management System
        </h1>
        <p style="color: #E1E8ED; margin: 0.5rem 0 0 0;">Comprehensive evidence handling for Indian courts and legal proceedings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize evidence manager
    if st.session_state.evidence_manager is None:
        with st.spinner("Initializing Legal Evidence Manager..."):
            st.session_state.evidence_manager = LegalEvidenceManager()
        st.success("✅ Legal Evidence Manager initialized")
    
    # Sidebar
    with st.sidebar:
        
        st.header("⚖️ Evidence Controls")
        
        # System status
        st.subheader("📊 System Status")
        summary = st.session_state.evidence_manager.get_evidence_summary()
        
        if not summary.get("error"):
            st.metric("Total Evidence", summary.get("total_evidence_items", 0))
            st.metric("Recent Submissions", summary.get("recent_court_submissions", 0))
            st.write(f"**Compliance:** {summary.get('compliance_level', 'Unknown')}")
            st.write(f"**Status:** {summary.get('system_status', 'Unknown')}")
        
        # Current case selection
        st.subheader("📁 Current Case")
        current_case = st.text_input(
            "Working Case Number",
            value=st.session_state.current_case,
            placeholder="FIR_2025_001"
        )
        st.session_state.current_case = current_case
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("📋 New Evidence Collection"):
            st.session_state.selected_evidence = None
        
        if st.button("🔍 Verify All Evidence"):
            verify_all_evidence()
        
        if st.button("📊 Generate Report"):
            generate_system_report()
        
        # Legal compliance info
        st.subheader("⚖️ Legal Compliance")
        st.info("""
        **Compliance Features:**
        ✅ Section 65B IT Act 2000
        ✅ Digital signatures
        ✅ Chain of custody
        ✅ Expert testimony prep
        ✅ Court formatting
        """)
    
    # Main content
    if st.session_state.selected_evidence:
        # Show evidence details
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Back to List"):
                st.session_state.selected_evidence = None
                st.rerun()
        
        display_evidence_details(st.session_state.selected_evidence)
    
    else:
        # Main dashboard
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Collect Evidence", 
            "📁 Evidence List", 
            "📊 Analytics", 
            "📚 Documentation"
        ])
        
        with tab1:
            display_evidence_collection_form()
        
        with tab2:
            # Load and display evidence
            if st.session_state.evidence_manager:
                df = load_evidence_data(st.session_state.evidence_manager.db_path)
                display_evidence_list(df)
        
        with tab3:
            # Analytics dashboard
            if st.session_state.evidence_manager:
                df = load_evidence_data(st.session_state.evidence_manager.db_path)
                display_analytics_dashboard(df)
        
        with tab4:
            # Documentation
            st.markdown("""
            ## ⚖️ Legal Evidence Management Documentation
            
            ### 🎯 **System Purpose**
            This system manages digital evidence collection, verification, and court preparation 
            according to Indian legal standards including the IT Act 2000 and Evidence Act 1872.
            
            ### 📋 **Evidence Collection Process**
            1. **Collect Evidence**: Gather digital evidence with proper documentation
            2. **Verify Integrity**: Cryptographic verification of evidence authenticity
            3. **Chain of Custody**: Maintain complete audit trail
            4. **Expert Analysis**: Prepare technical testimony
            5. **Court Formatting**: Create legal-compliant submission packages
            
            ### 🔐 **Security Features**
            - **Digital Signatures**: Cryptographic proof of authenticity
            - **Hash Verification**: Detect any alterations to evidence
            - **Encrypted Storage**: Secure evidence preservation
            - **Access Logging**: Complete audit trail
            
            ### ⚖️ **Legal Compliance**
            - **Section 65B Certificates**: IT Act 2000 compliance
            - **Expert Testimony**: Technical analysis for court
            - **Chain of Custody**: Forensic evidence handling
            - **Court Formatting**: Ready-to-submit packages
            
            ### 📞 **Support**
            - **Technical Support**: 1-800-EVIDENCE-HELP
            - **Legal Guidance**: expert@police-ai-monitor.gov.in
            - **Training**: Complete user manuals included
            """)

def verify_all_evidence():
    """Verify integrity of all evidence"""
    if not st.session_state.evidence_manager:
        st.error("Evidence manager not initialized")
        return
    
    df = load_evidence_data(st.session_state.evidence_manager.db_path)
    
    if df.empty:
        st.info("No evidence to verify")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    verified_count = 0
    failed_count = 0
    
    for i, evidence in df.iterrows():
        status_text.text(f"Verifying evidence {i+1}/{len(df)}: {evidence['evidence_id']}")
        
        verification_results = st.session_state.evidence_manager.verify_evidence_integrity(evidence['evidence_id'])
        
        if verification_results.get("integrity_score", 0) >= 0.8:
            verified_count += 1
        else:
            failed_count += 1
        
        progress_bar.progress((i + 1) / len(df))
    
    status_text.text("Verification complete!")
    st.success(f"✅ Verified {verified_count} evidence items, {failed_count} failed verification")

def generate_system_report():
    """Generate comprehensive system report"""
    if not st.session_state.evidence_manager:
        st.error("Evidence manager not initialized")
        return
    
    summary = st.session_state.evidence_manager.get_evidence_summary()
    df = load_evidence_data(st.session_state.evidence_manager.db_path)
    
    report = f"""
# Legal Evidence Management System Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Overview
- Total Evidence Items: {summary.get('total_evidence_items', 0)}
- Active Cases: {df['case_number'].nunique() if not df.empty else 0}
- Court-Ready Items: {df['court_formatted'].sum() if not df.empty else 0}
- Recent Submissions: {summary.get('recent_court_submissions', 0)}

## Compliance Status
- System Status: {summary.get('system_status', 'Unknown')}
- Compliance Level: {summary.get('compliance_level', 'Unknown')}
- Chain of Custody Entries: {summary.get('total_custody_entries', 0)}

## Evidence Distribution
{summary.get('status_distribution', {})}

## Recommendations
- Ensure regular integrity verification
- Maintain proper chain of custody
- Prepare expert testimony in advance
- Keep court packages updated
"""
    
    st.download_button(
        "⬇️ Download System Report",
        data=report,
        file_name=f"evidence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()
