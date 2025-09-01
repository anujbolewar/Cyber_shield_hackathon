#!/usr/bin/env python3
"""
🏛️ POLICE WORKFLOW INTEGRATION PAGE
Streamlit interface for comprehensive police workflow optimization
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

try:
    from police_workflow_optimizer import PoliceWorkflowOptimizer
except ImportError:
    st.error("⚠️ Police Workflow Optimizer not available. Please check installation.")
    st.stop()

def main():
    st.set_page_config(
        page_title="🏛️ Police Workflow Optimizer",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for police theme
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ POLICE WORKFLOW OPTIMIZER</h1>
        <p>Comprehensive Workflow Management for Indian Police Departments</p>
        <p>📋 FIR Integration • 🔐 Evidence Chain • ⚖️ Court Management • 📊 Performance Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize optimizer
    if 'workflow_optimizer' not in st.session_state:
        st.session_state.workflow_optimizer = PoliceWorkflowOptimizer()
    
    optimizer = st.session_state.workflow_optimizer
    
    # Sidebar navigation
    st.sidebar.title("🏛️ Workflow Management")
    
    workflow_option = st.sidebar.selectbox(
        "Select Workflow Function",
        [
            "📊 Dashboard Overview",
            "📋 FIR Integration & Tracking",
            "🔐 Evidence Chain of Custody",
            "⚖️ Court Date Management",
            "🔄 Shift Handover Reports",
            "⬆️ Senior Officer Escalation",
            "🚨 Inter-District Alerts",
            "⚖️ Legal Compliance Checklist",
            "📊 Performance Metrics",
            "🧪 System Testing"
        ]
    )
    
    # Dashboard Overview
    if workflow_option == "📊 Dashboard Overview":
        display_dashboard_overview(optimizer)
    
    # FIR Integration
    elif workflow_option == "📋 FIR Integration & Tracking":
        display_fir_integration(optimizer)
    
    # Evidence Chain
    elif workflow_option == "🔐 Evidence Chain of Custody":
        display_evidence_chain(optimizer)
    
    # Court Management
    elif workflow_option == "⚖️ Court Date Management":
        display_court_management(optimizer)
    
    # Shift Handover
    elif workflow_option == "🔄 Shift Handover Reports":
        display_shift_handover(optimizer)
    
    # Escalation Workflow
    elif workflow_option == "⬆️ Senior Officer Escalation":
        display_escalation_workflow(optimizer)
    
    # Inter-District Alerts
    elif workflow_option == "🚨 Inter-District Alerts":
        display_inter_district_alerts(optimizer)
    
    # Legal Compliance
    elif workflow_option == "⚖️ Legal Compliance Checklist":
        display_legal_compliance(optimizer)
    
    # Performance Metrics
    elif workflow_option == "📊 Performance Metrics":
        display_performance_metrics(optimizer)
    
    # System Testing
    elif workflow_option == "🧪 System Testing":
        display_system_testing(optimizer)

def display_dashboard_overview(optimizer):
    """Display comprehensive dashboard overview"""
    st.header("📊 Police Workflow Dashboard")
    
    # Get dashboard summary
    dashboard_data = optimizer.get_workflow_dashboard_summary()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📋 Total FIRs",
            dashboard_data.get('fir_management', {}).get('total_firs', 0),
            delta=f"{dashboard_data.get('fir_management', {}).get('active_investigations', 0)} Active"
        )
    
    with col2:
        st.metric(
            "🔐 Evidence Items",
            dashboard_data.get('evidence_management', {}).get('total_evidence_items', 0),
            delta=f"{dashboard_data.get('evidence_management', {}).get('items_in_custody', 0)} In Custody"
        )
    
    with col3:
        st.metric(
            "⚖️ Court Hearings",
            dashboard_data.get('court_management', {}).get('upcoming_hearings', 0),
            delta="Upcoming"
        )
    
    with col4:
        st.metric(
            "📊 Avg Performance",
            f"{dashboard_data.get('performance_overview', {}).get('average_performance_score', 0):.1f}%",
            delta=dashboard_data.get('performance_overview', {}).get('department_grade', 'N/A')
        )
    
    # Performance overview charts
    st.subheader("📈 Performance Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sample data for FIR completion rates
        fir_data = {
            'Status': ['Completed', 'Under Investigation', 'Pending'],
            'Count': [15, 8, 3],
            'Percentage': [57.7, 30.8, 11.5]
        }
        
        fig_pie = px.pie(
            values=fir_data['Count'],
            names=fir_data['Status'],
            title="FIR Status Distribution",
            color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Sample data for performance trends
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        performance_scores = [78, 82, 85, 88, 86, 90]
        
        fig_line = px.line(
            x=months,
            y=performance_scores,
            title="Monthly Performance Trend",
            markers=True
        )
        fig_line.update_layout(
            xaxis_title="Month",
            yaxis_title="Performance Score (%)"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Recent activities
    st.subheader("🔄 Recent Workflow Activities")
    
    recent_activities = [
        {"Time": "2 hours ago", "Activity": "FIR registered for cyber fraud case", "Officer": "Inspector Priya Sharma", "Status": "✅ Completed"},
        {"Time": "4 hours ago", "Activity": "Evidence custody transferred", "Officer": "Head Constable Amit Singh", "Status": "🔄 In Progress"},
        {"Time": "6 hours ago", "Activity": "Court hearing scheduled", "Officer": "Inspector Rajesh Kumar", "Status": "📅 Scheduled"},
        {"Time": "8 hours ago", "Activity": "Inter-district alert sent", "Officer": "ACP Cyber Crime", "Status": "🚨 Active"},
        {"Time": "1 day ago", "Activity": "Performance evaluation completed", "Officer": "DCP Cyber Division", "Status": "📊 Reviewed"}
    ]
    
    activities_df = pd.DataFrame(recent_activities)
    st.dataframe(activities_df, use_container_width=True)

def display_fir_integration(optimizer):
    """Display FIR integration and tracking interface"""
    st.header("📋 FIR Integration & Case Tracking")
    
    tab1, tab2 = st.tabs(["🆕 Register New FIR", "📊 Track Existing FIRs"])
    
    with tab1:
        st.subheader("Register New FIR")
        
        with st.form("fir_registration"):
            col1, col2 = st.columns(2)
            
            with col1:
                police_station = st.text_input("Police Station", value="Cyber Crime Cell Mumbai")
                district = st.text_input("District", value="Mumbai")
                state = st.selectbox("State", ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Gujarat"])
                complainant_name = st.text_input("Complainant Name")
                complainant_contact = st.text_input("Complainant Contact")
            
            with col2:
                offense_type = st.selectbox(
                    "Offense Type",
                    ["CYBER_FRAUD", "IDENTITY_THEFT", "ONLINE_HARASSMENT", "FINANCIAL_FRAUD", "DATA_THEFT", "RANSOMWARE"]
                )
                ipc_sections = st.text_input("IPC/IT Act Sections", value="420, 66C IT Act")
                investigation_officer = st.text_input("Investigation Officer")
                officer_contact = st.text_input("Officer Contact")
                priority_level = st.selectbox("Priority Level", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
            
            submitted = st.form_submit_button("📋 Register FIR")
            
            if submitted:
                fir_data = {
                    'police_station': police_station,
                    'district': district,
                    'state': state,
                    'complainant_name': complainant_name,
                    'complainant_contact': complainant_contact,
                    'offense_type': offense_type,
                    'ipc_sections': ipc_sections,
                    'investigation_officer': investigation_officer,
                    'officer_contact': officer_contact,
                    'priority_level': priority_level
                }
                
                result = optimizer.fir_integration_tracking(fir_data)
                
                if result.get('success'):
                    st.success(f"✅ FIR registered successfully!")
                    st.json(result)
                else:
                    st.error(f"❌ FIR registration failed: {result.get('error')}")
    
    with tab2:
        st.subheader("FIR Tracking Dashboard")
        
        # Sample FIR data for display
        sample_firs = [
            {
                "FIR Number": "FIR_CYB_2024_A1B2C3D4",
                "Date": "2024-01-15",
                "Offense": "CYBER_FRAUD",
                "Status": "UNDER_INVESTIGATION",
                "Priority": "HIGH",
                "Officer": "Inspector Priya Sharma"
            },
            {
                "FIR Number": "FIR_CYB_2024_E5F6G7H8",
                "Date": "2024-01-14",
                "Offense": "IDENTITY_THEFT",
                "Status": "CHARGE_SHEET_FILED",
                "Priority": "MEDIUM",
                "Officer": "Inspector Rajesh Kumar"
            }
        ]
        
        firs_df = pd.DataFrame(sample_firs)
        st.dataframe(firs_df, use_container_width=True)

def display_evidence_chain(optimizer):
    """Display evidence chain of custody interface"""
    st.header("🔐 Evidence Chain of Custody")
    
    tab1, tab2 = st.tabs(["📥 Record Evidence Custody", "🔍 Track Evidence Chain"])
    
    with tab1:
        st.subheader("Record Evidence Custody")
        
        with st.form("evidence_custody"):
            col1, col2 = st.columns(2)
            
            with col1:
                fir_number = st.text_input("FIR Number")
                evidence_id = st.text_input("Evidence ID", value="DEVICE_001")
                evidence_type = st.selectbox(
                    "Evidence Type",
                    ["DIGITAL_DEVICE", "DOCUMENTS", "PHOTOGRAPHS", "AUDIO_RECORDING", "VIDEO_RECORDING", "DIGITAL_FILES"]
                )
                evidence_description = st.text_area("Evidence Description")
            
            with col2:
                custody_officer = st.text_input("Custody Officer")
                custody_officer_id = st.text_input("Officer ID")
                location_stored = st.text_input("Storage Location", value="Evidence Room A-1")
                witness_officer = st.text_input("Witness Officer (Optional)")
            
            custody_notes = st.text_area("Custody Notes")
            
            submitted = st.form_submit_button("🔐 Record Custody")
            
            if submitted:
                custody_data = {
                    'fir_number': fir_number,
                    'evidence_id': evidence_id,
                    'evidence_type': evidence_type,
                    'evidence_description': evidence_description,
                    'custody_officer': custody_officer,
                    'custody_officer_id': custody_officer_id,
                    'location_stored': location_stored,
                    'witness_officer': witness_officer,
                    'custody_notes': custody_notes
                }
                
                result = optimizer.evidence_chain_custody_logging(custody_data)
                
                if result.get('success'):
                    st.success("✅ Evidence custody recorded successfully!")
                    st.json(result)
                else:
                    st.error(f"❌ Custody recording failed: {result.get('error')}")
    
    with tab2:
        st.subheader("Evidence Chain Tracking")
        
        # Sample evidence chain data
        evidence_chain = [
            {
                "Custody ID": "CUSTODY_A1B2C3D4E5F6",
                "Evidence ID": "MOBILE_001",
                "Officer": "HC Amit Singh",
                "Start Time": "2024-01-15 10:00:00",
                "Location": "Evidence Room A-1",
                "Status": "IN_CUSTODY"
            },
            {
                "Custody ID": "CUSTODY_F6E5D4C3B2A1",
                "Evidence ID": "LAPTOP_002",
                "Officer": "Constable Neha Patel",
                "Start Time": "2024-01-14 14:30:00",
                "Location": "Forensic Lab",
                "Status": "UNDER_EXAMINATION"
            }
        ]
        
        evidence_df = pd.DataFrame(evidence_chain)
        st.dataframe(evidence_df, use_container_width=True)

def display_court_management(optimizer):
    """Display court date management interface"""
    st.header("⚖️ Court Date Management")
    
    tab1, tab2 = st.tabs(["📅 Schedule Court Date", "📋 Court Calendar"])
    
    with tab1:
        st.subheader("Schedule Court Hearing")
        
        with st.form("court_scheduling"):
            col1, col2 = st.columns(2)
            
            with col1:
                fir_number = st.text_input("FIR Number")
                case_number = st.text_input("Case Number (Optional)")
                court_name = st.text_input("Court Name", value="Metropolitan Magistrate Court")
                court_type = st.selectbox("Court Type", ["MAGISTRATE", "SESSIONS", "HIGH_COURT", "SUPREME_COURT"])
            
            with col2:
                hearing_date = st.date_input("Hearing Date", value=datetime.now().date() + timedelta(days=30))
                hearing_time = st.time_input("Hearing Time", value=datetime.strptime("10:00", "%H:%M").time())
                case_stage = st.selectbox(
                    "Case Stage",
                    ["PRELIMINARY", "CHARGE_SHEET_FILING", "EVIDENCE_RECORDING", "ARGUMENTS", "JUDGMENT"]
                )
                officer_required = st.text_input("Officer Required for Appearance")
            
            prosecutor_name = st.text_input("Prosecutor Name (Optional)")
            defense_lawyer = st.text_input("Defense Lawyer (Optional)")
            notes = st.text_area("Additional Notes")
            
            submitted = st.form_submit_button("📅 Schedule Hearing")
            
            if submitted:
                court_data = {
                    'fir_number': fir_number,
                    'case_number': case_number,
                    'court_name': court_name,
                    'court_type': court_type,
                    'hearing_date': hearing_date.isoformat(),
                    'hearing_time': hearing_time.strftime("%H:%M"),
                    'case_stage': case_stage,
                    'officer_required': officer_required,
                    'prosecutor_name': prosecutor_name,
                    'defense_lawyer': defense_lawyer,
                    'notes': notes
                }
                
                result = optimizer.court_date_reminders_and_preparation(court_data)
                
                if result.get('success'):
                    st.success("✅ Court hearing scheduled successfully!")
                    st.json(result)
                else:
                    st.error(f"❌ Court scheduling failed: {result.get('error')}")
    
    with tab2:
        st.subheader("Upcoming Court Hearings")
        
        # Sample court calendar data
        court_calendar = [
            {
                "Date": "2024-01-20",
                "Time": "10:30",
                "Court": "Metropolitan Magistrate",
                "Case": "FIR_CYB_2024_A1B2C3D4",
                "Stage": "CHARGE_SHEET_FILING",
                "Officer": "Inspector Priya Sharma"
            },
            {
                "Date": "2024-01-22",
                "Time": "11:00",
                "Court": "Sessions Court",
                "Case": "FIR_CYB_2024_E5F6G7H8",
                "Stage": "EVIDENCE_RECORDING",
                "Officer": "Inspector Rajesh Kumar"
            }
        ]
        
        court_df = pd.DataFrame(court_calendar)
        st.dataframe(court_df, use_container_width=True)
        
        # Reminder settings
        st.subheader("📱 Reminder Settings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.checkbox("1 Week Before", value=True)
        with col2:
            st.checkbox("3 Days Before", value=True)
        with col3:
            st.checkbox("1 Day Before", value=True)

def display_shift_handover(optimizer):
    """Display shift handover interface"""
    st.header("🔄 Shift Handover Reports")
    
    with st.form("shift_handover"):
        st.subheader("Record Shift Handover")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Outgoing Officer Details**")
            outgoing_officer = st.text_input("Outgoing Officer Name")
            outgoing_officer_id = st.text_input("Outgoing Officer ID")
            shift_date = st.date_input("Shift Date", value=datetime.now().date())
        
        with col2:
            st.write("**Incoming Officer Details**")
            incoming_officer = st.text_input("Incoming Officer Name")
            incoming_officer_id = st.text_input("Incoming Officer ID")
            shift_type = st.selectbox("Shift Type", ["DAY_TO_NIGHT", "NIGHT_TO_DAY", "EMERGENCY", "REGULAR"])
        
        department = st.text_input("Department", value="CYBER_CRIME_CELL")
        
        col1, col2 = st.columns(2)
        
        with col1:
            active_cases = st.text_area("Active Cases (one per line)").split('\n') if st.text_area("Active Cases (one per line)") else []
            pending_tasks = st.text_area("Pending Tasks (one per line)").split('\n') if st.text_area("Pending Tasks (one per line)") else []
        
        with col2:
            urgent_matters = st.text_area("Urgent Matters (one per line)").split('\n') if st.text_area("Urgent Matters (one per line)") else []
            ongoing_operations = st.text_area("Ongoing Operations (one per line)").split('\n') if st.text_area("Ongoing Operations (one per line)") else []
        
        equipment_status = st.selectbox("Equipment Status", ["ALL_OPERATIONAL", "MINOR_ISSUES", "MAJOR_ISSUES", "CRITICAL_FAILURE"])
        security_briefing = st.text_area("Security Briefing")
        notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("🔄 Complete Handover")
        
        if submitted:
            handover_data = {
                'outgoing_officer': outgoing_officer,
                'outgoing_officer_id': outgoing_officer_id,
                'incoming_officer': incoming_officer,
                'incoming_officer_id': incoming_officer_id,
                'shift_date': shift_date.isoformat(),
                'shift_type': shift_type,
                'department': department,
                'active_cases': [case.strip() for case in active_cases if case.strip()],
                'pending_tasks': [task.strip() for task in pending_tasks if task.strip()],
                'urgent_matters': [matter.strip() for matter in urgent_matters if matter.strip()],
                'ongoing_operations': [op.strip() for op in ongoing_operations if op.strip()],
                'equipment_status': equipment_status,
                'security_briefing': security_briefing,
                'notes': notes
            }
            
            result = optimizer.shift_handover_reports(handover_data)
            
            if result.get('success'):
                st.success("✅ Shift handover completed successfully!")
                st.json(result)
            else:
                st.error(f"❌ Handover recording failed: {result.get('error')}")

def display_escalation_workflow(optimizer):
    """Display escalation workflow interface"""
    st.header("⬆️ Senior Officer Escalation Workflow")
    
    with st.form("escalation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            fir_number = st.text_input("FIR Number (Optional)")
            case_id = st.text_input("Case ID (Optional)")
            escalation_type = st.selectbox(
                "Escalation Type",
                ["INVESTIGATION_DELAY", "RESOURCE_REQUIREMENT", "INTER_STATE_COORDINATION", "TECHNICAL_EXPERTISE", "LEGAL_GUIDANCE", "EMERGENCY_SITUATION"]
            )
            escalation_reason = st.text_area("Escalation Reason")
        
        with col2:
            escalated_by = st.text_input("Escalated By")
            escalated_by_id = st.text_input("Escalating Officer ID")
            escalated_to = st.text_input("Escalated To")
            escalated_to_id = st.text_input("Senior Officer ID")
            escalation_level = st.selectbox("Escalation Level", ["LEVEL_1", "LEVEL_2", "LEVEL_3", "LEVEL_4", "LEVEL_5"])
            urgency_level = st.selectbox("Urgency Level", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        
        escalation_notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("⬆️ Initiate Escalation")
        
        if submitted:
            escalation_data = {
                'fir_number': fir_number,
                'case_id': case_id,
                'escalation_type': escalation_type,
                'escalation_reason': escalation_reason,
                'escalated_by': escalated_by,
                'escalated_by_id': escalated_by_id,
                'escalated_to': escalated_to,
                'escalated_to_id': escalated_to_id,
                'escalation_level': escalation_level,
                'urgency_level': urgency_level,
                'escalation_notes': escalation_notes
            }
            
            result = optimizer.senior_officer_escalation_workflow(escalation_data)
            
            if result.get('success'):
                st.success("✅ Escalation initiated successfully!")
                st.json(result)
            else:
                st.error(f"❌ Escalation failed: {result.get('error')}")

def display_inter_district_alerts(optimizer):
    """Display inter-district alert sharing interface"""
    st.header("🚨 Inter-District Alert Sharing")
    
    with st.form("alert_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            source_district = st.text_input("Source District", value="Mumbai Cyber Crime")
            source_state = st.text_input("Source State", value="Maharashtra")
            alert_type = st.selectbox(
                "Alert Type",
                ["CYBER_FRAUD_NETWORK", "WANTED_CRIMINAL", "STOLEN_VEHICLE", "TERRORISM_THREAT", "ORGANIZED_CRIME", "MISSING_PERSON"]
            )
            alert_priority = st.selectbox("Alert Priority", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        
        with col2:
            target_districts = st.multiselect(
                "Target Districts",
                ["Delhi Cyber Crime", "Bangalore Cyber Crime", "Pune Cyber Crime", "Chennai Cyber Crime", "Hyderabad Cyber Crime"]
            )
            validity_hours = st.number_input("Validity (Hours)", min_value=1, max_value=168, value=72)
            coordination_officer = st.text_input("Coordination Officer")
            coordination_contact = st.text_input("Coordination Contact")
        
        alert_title = st.text_input("Alert Title")
        alert_description = st.text_area("Alert Description")
        suspect_details = st.text_area("Suspect Details (Optional)")
        vehicle_details = st.text_area("Vehicle Details (Optional)")
        area_of_operation = st.text_input("Area of Operation (Optional)")
        
        submitted = st.form_submit_button("🚨 Send Alert")
        
        if submitted:
            alert_data = {
                'source_district': source_district,
                'source_state': source_state,
                'target_districts': target_districts,
                'alert_type': alert_type,
                'alert_priority': alert_priority,
                'alert_title': alert_title,
                'alert_description': alert_description,
                'suspect_details': suspect_details,
                'vehicle_details': vehicle_details,
                'area_of_operation': area_of_operation,
                'validity_hours': validity_hours,
                'coordination_officer': coordination_officer,
                'coordination_contact': coordination_contact
            }
            
            result = optimizer.inter_district_alert_sharing(alert_data)
            
            if result.get('success'):
                st.success("✅ Inter-district alert sent successfully!")
                st.json(result)
            else:
                st.error(f"❌ Alert sending failed: {result.get('error')}")

def display_legal_compliance(optimizer):
    """Display legal compliance checklist interface"""
    st.header("⚖️ Legal Compliance Checklist Automation")
    
    with st.form("compliance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            fir_number = st.text_input("FIR Number")
            compliance_type = st.selectbox(
                "Compliance Type",
                ["CYBER_CRIME", "FINANCIAL_FRAUD", "TERRORISM"]
            )
            compliance_officer = st.text_input("Compliance Officer")
        
        with col2:
            legal_reviewer = st.text_input("Legal Reviewer (Optional)")
            deadline_days = st.number_input("Deadline (Days)", min_value=1, max_value=365, value=90)
            compliance_notes = st.text_area("Compliance Notes")
        
        submitted = st.form_submit_button("⚖️ Create Compliance Checklist")
        
        if submitted:
            compliance_data = {
                'fir_number': fir_number,
                'compliance_type': compliance_type,
                'compliance_officer': compliance_officer,
                'legal_reviewer': legal_reviewer,
                'compliance_notes': compliance_notes
            }
            
            result = optimizer.legal_compliance_checklist_automation(compliance_data)
            
            if result.get('success'):
                st.success("✅ Legal compliance checklist created successfully!")
                
                # Display checklist items
                st.subheader("📋 Legal Requirements Checklist")
                requirements = result.get('legal_requirements', [])
                
                for i, requirement in enumerate(requirements):
                    st.checkbox(f"{requirement}", key=f"req_{i}")
                
                st.json(result)
            else:
                st.error(f"❌ Compliance checklist creation failed: {result.get('error')}")

def display_performance_metrics(optimizer):
    """Display performance metrics interface"""
    st.header("📊 Cyber Cell Performance Metrics")
    
    with st.form("performance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            officer_id = st.text_input("Officer ID")
            officer_name = st.text_input("Officer Name")
            department = st.text_input("Department", value="CYBER_CRIME_CELL")
            evaluation_period = st.text_input("Evaluation Period", value=f"{datetime.now().year}-Q{(datetime.now().month-1)//3 + 1}")
        
        with col2:
            cases_handled = st.number_input("Cases Handled", min_value=0, value=25)
            cases_solved = st.number_input("Cases Solved", min_value=0, value=20)
            cases_pending = st.number_input("Cases Pending", min_value=0, value=5)
            average_resolution_time = st.number_input("Average Resolution Time (Days)", min_value=0.0, value=22.5)
        
        st.subheader("📊 Performance Scores (0-100)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            evidence_quality_score = st.slider("Evidence Quality Score", 0.0, 100.0, 88.0)
            court_appearance_rate = st.slider("Court Appearance Rate", 0.0, 100.0, 92.0)
        
        with col2:
            compliance_adherence = st.slider("Compliance Adherence", 0.0, 100.0, 95.0)
            inter_agency_coordination = st.slider("Inter-Agency Coordination", 0.0, 100.0, 85.0)
        
        with col3:
            citizen_satisfaction = st.slider("Citizen Satisfaction", 0.0, 100.0, 89.0)
        
        supervisor_comments = st.text_area("Supervisor Comments")
        improvement_areas = st.text_area("Improvement Areas")
        commendations = st.text_area("Commendations")
        training_required = st.text_area("Training Required")
        
        submitted = st.form_submit_button("📊 Generate Performance Evaluation")
        
        if submitted:
            performance_data = {
                'officer_id': officer_id,
                'officer_name': officer_name,
                'department': department,
                'evaluation_period': evaluation_period,
                'cases_handled': cases_handled,
                'cases_solved': cases_solved,
                'cases_pending': cases_pending,
                'average_resolution_time': average_resolution_time,
                'evidence_quality_score': evidence_quality_score,
                'court_appearance_rate': court_appearance_rate,
                'compliance_adherence': compliance_adherence,
                'inter_agency_coordination': inter_agency_coordination,
                'citizen_satisfaction': citizen_satisfaction,
                'supervisor_comments': supervisor_comments,
                'improvement_areas': improvement_areas,
                'commendations': commendations,
                'training_required': training_required
            }
            
            result = optimizer.cyber_cell_performance_metrics(performance_data)
            
            if result.get('success'):
                st.success("✅ Performance evaluation completed successfully!")
                
                # Display performance summary
                st.subheader("📊 Performance Summary")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Overall Score",
                        f"{result.get('performance_summary', {}).get('overall_score', 0):.1f}%",
                        delta=result.get('performance_summary', {}).get('performance_grade', 'N/A')
                    )
                
                with col2:
                    st.metric(
                        "Cases Solved Rate",
                        f"{result.get('performance_summary', {}).get('cases_solved_rate', 0):.1f}%"
                    )
                
                with col3:
                    st.metric(
                        "Avg Resolution",
                        f"{result.get('performance_summary', {}).get('average_resolution_days', 0):.1f} days"
                    )
                
                st.json(result)
            else:
                st.error(f"❌ Performance evaluation failed: {result.get('error')}")

def display_system_testing(optimizer):
    """Display system testing interface"""
    st.header("🧪 System Testing & Validation")
    
    if st.button("🧪 Run Complete System Test"):
        with st.spinner("Running comprehensive workflow optimizer tests..."):
            
            # Test data for demonstration
            test_results = []
            
            # Test 1: FIR Integration
            st.write("📋 Testing FIR Integration...")
            fir_test_data = {
                'police_station': 'Test Cyber Cell',
                'district': 'Test District',
                'state': 'Test State',
                'complainant_name': 'Test Complainant',
                'complainant_contact': '+919999999999',
                'offense_type': 'CYBER_FRAUD',
                'ipc_sections': '420, 66C IT Act',
                'investigation_officer': 'Test Officer',
                'officer_contact': '+919999999998',
                'priority_level': 'HIGH'
            }
            
            fir_result = optimizer.fir_integration_tracking(fir_test_data)
            test_results.append(("FIR Integration", fir_result.get('success', False)))
            
            if fir_result.get('success'):
                st.success("✅ FIR Integration: PASSED")
            else:
                st.error("❌ FIR Integration: FAILED")
            
            # Test 2: Evidence Chain
            st.write("🔐 Testing Evidence Chain...")
            custody_test_data = {
                'fir_number': fir_result.get('fir_number', 'TEST_FIR'),
                'evidence_id': 'TEST_EVIDENCE_001',
                'evidence_type': 'DIGITAL_DEVICE',
                'evidence_description': 'Test mobile device',
                'custody_officer': 'Test Officer',
                'custody_officer_id': 'TEST001',
                'location_stored': 'Test Evidence Room'
            }
            
            custody_result = optimizer.evidence_chain_custody_logging(custody_test_data)
            test_results.append(("Evidence Chain", custody_result.get('success', False)))
            
            if custody_result.get('success'):
                st.success("✅ Evidence Chain: PASSED")
            else:
                st.error("❌ Evidence Chain: FAILED")
            
            # Continue with other tests...
            
            # Display summary
            st.subheader("🎯 Test Summary")
            
            passed_tests = sum(1 for _, success in test_results if success)
            total_tests = len(test_results)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Tests", total_tests)
            
            with col2:
                st.metric("Passed", passed_tests, delta=f"{passed_tests/total_tests*100:.1f}%")
            
            with col3:
                st.metric("Failed", total_tests - passed_tests)
            
            # Test results table
            results_df = pd.DataFrame(test_results, columns=["Test", "Status"])
            results_df["Status"] = results_df["Status"].map({True: "✅ PASSED", False: "❌ FAILED"})
            st.dataframe(results_df, use_container_width=True)

if __name__ == "__main__":
    main()
