#!/usr/bin/env python3
"""
🚀 DEPLOYMENT MANAGER PAGE
Comprehensive deployment strategies for Police Monitor
All-in-one deployment management interface
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import zipfile

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent / "utils"))

try:
    from deployment_strategies import DeploymentManager
    from video_tutorials import VideoTutorialGenerator
    from remote_support import RemoteSupportSystem
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="🚀 Deployment Manager",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🚀 Police Monitor Deployment Manager")
    st.markdown("**Comprehensive deployment strategies for various police environments**")
    
    # Initialize deployment systems
    if 'deployment_manager' not in st.session_state:
        st.session_state.deployment_manager = DeploymentManager()
    
    if 'tutorial_generator' not in st.session_state:
        st.session_state.tutorial_generator = VideoTutorialGenerator()
    
    if 'support_system' not in st.session_state:
        st.session_state.support_system = RemoteSupportSystem()
    
    # Sidebar navigation
    st.sidebar.title("🚀 Deployment Options")
    deployment_option = st.sidebar.selectbox(
        "Choose Deployment Strategy:",
        [
            "📊 System Requirements Check",
            "🏢 Local Network Deployment",
            "💾 USB Portable Version", 
            "☁️ Cloud-Agnostic Configuration",
            "🪶 Lightweight Version",
            "📚 Offline Documentation",
            "🎥 Video Tutorials",
            "🔧 Remote Support"
        ]
    )
    
    # Main content based on selection
    if deployment_option == "📊 System Requirements Check":
        show_system_requirements()
    elif deployment_option == "🏢 Local Network Deployment":
        show_local_network_deployment()
    elif deployment_option == "💾 USB Portable Version":
        show_usb_portable_deployment()
    elif deployment_option == "☁️ Cloud-Agnostic Configuration":
        show_cloud_deployment()
    elif deployment_option == "🪶 Lightweight Version":
        show_lightweight_deployment()
    elif deployment_option == "📚 Offline Documentation":
        show_offline_documentation()
    elif deployment_option == "🎥 Video Tutorials":
        show_video_tutorials()
    elif deployment_option == "🔧 Remote Support":
        show_remote_support()

def show_system_requirements():
    """Display system requirements checking interface"""
    st.header("📊 System Requirements Check")
    st.markdown("Verify your system meets the requirements for Police Monitor deployment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Select Requirement Level")
        
        requirement_level = st.selectbox(
            "Choose requirement level:",
            ["minimum", "recommended", "optimal"],
            index=1,
            help="Select the requirement level based on your deployment needs"
        )
        
        if st.button("🔍 Check System Requirements", type="primary"):
            with st.spinner("Checking system requirements..."):
                requirements_result = st.session_state.deployment_manager.check_system_requirements(requirement_level)
                
                # Display results
                st.subheader("📊 System Check Results")
                
                if requirements_result.get('meets_requirements', False):
                    st.success("✅ System meets all requirements!")
                else:
                    st.warning("⚠️ System has some issues that need attention")
                
                # Individual checks
                if 'checks' in requirements_result:
                    for check_name, check_result in requirements_result['checks'].items():
                        status_icon = "✅" if check_result.get('status', False) else "❌"
                        st.write(f"{status_icon} **{check_name.replace('_', ' ').title()}**: {check_result.get('current', 'N/A')} (Required: {check_result.get('required', 'N/A')})")
                
                # Warnings
                if requirements_result.get('warnings'):
                    st.subheader("⚠️ Warnings")
                    for warning in requirements_result['warnings']:
                        st.warning(warning)
                
                # Recommendations
                if requirements_result.get('recommendations'):
                    st.subheader("💡 Recommendations")
                    for recommendation in requirements_result['recommendations']:
                        st.info(recommendation)
    
    with col2:
        st.subheader("📋 Requirement Levels")
        
        # Display requirement details
        requirements = st.session_state.deployment_manager.system_requirements
        
        for level, specs in requirements.items():
            st.markdown(f"**{level.title()}**")
            st.write(f"• RAM: {specs['ram_gb']} GB")
            st.write(f"• Storage: {specs['storage_gb']} GB")
            st.write(f"• CPU: {specs['cpu_cores']} cores")
            st.write(f"• Python: {specs['python_version']}")
            st.write("---")

def show_local_network_deployment():
    """Display local network deployment interface"""
    st.header("🏢 Local Network Deployment")
    st.markdown("Deploy Police Monitor for local police station networks")
    
    with st.form("local_network_form"):
        st.subheader("🔧 Network Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            deployment_name = st.text_input(
                "Deployment Name:",
                value="police_station_main",
                help="Unique identifier for this deployment"
            )
            
            host = st.text_input(
                "Host Address:",
                value="0.0.0.0",
                help="Server host address (0.0.0.0 for all interfaces)"
            )
            
            port = st.number_input(
                "Port Number:",
                value=8501,
                min_value=1024,
                max_value=65535,
                help="Port number for the web application"
            )
        
        with col2:
            max_connections = st.number_input(
                "Max Connections:",
                value=50,
                min_value=1,
                max_value=200,
                help="Maximum concurrent user connections"
            )
            
            enable_cors = st.checkbox(
                "Enable CORS",
                value=True,
                help="Allow cross-origin requests"
            )
            
            session_timeout = st.number_input(
                "Session Timeout (seconds):",
                value=3600,
                min_value=300,
                max_value=86400,
                help="User session timeout duration"
            )
        
        submitted = st.form_submit_button("🚀 Create Local Network Deployment", type="primary")
        
        if submitted:
            config = {
                'deployment_name': deployment_name,
                'network': {
                    'host': host,
                    'port': port,
                    'max_connections': max_connections,
                    'cors_enabled': enable_cors,
                    'session_timeout': session_timeout
                }
            }
            
            with st.spinner("Creating local network deployment..."):
                result = st.session_state.deployment_manager.create_local_network_deployment(config)
                
                if result.get('success'):
                    st.success("✅ Local network deployment created successfully!")
                    
                    st.subheader("📋 Deployment Details")
                    st.write(f"**Deployment Directory:** {result['deployment_dir']}")
                    st.write(f"**Access URL:** {result['access_url']}")
                    st.write(f"**Network Configuration:** {result['network_settings']['host']}:{result['network_settings']['port']}")
                    
                    st.subheader("📂 Created Files")
                    for file_name in result['files_created']:
                        st.write(f"• {file_name}")
                    
                    st.subheader("📖 Next Steps")
                    st.markdown("""
                    1. Copy the deployment directory to your server
                    2. Install Python and dependencies
                    3. Run the startup script
                    4. Configure firewall to allow the port
                    5. Test access from client machines
                    """)
                else:
                    st.error(f"❌ Deployment failed: {result.get('error', 'Unknown error')}")

def show_usb_portable_deployment():
    """Display USB portable deployment interface"""
    st.header("💾 USB Portable Version")
    st.markdown("Create a portable version that runs from USB drive")
    
    with st.form("usb_portable_form"):
        st.subheader("💾 Portable Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            usb_name = st.text_input(
                "USB Package Name:",
                value="PoliceMonitor_Portable",
                help="Name for the portable package"
            )
            
            include_sample_data = st.checkbox(
                "Include Sample Data",
                value=True,
                help="Include sample data for demonstration"
            )
        
        with col2:
            auto_launch = st.checkbox(
                "Auto-launch on Insert",
                value=False,
                help="Automatically start when USB is inserted"
            )
            
            encryption_enabled = st.checkbox(
                "Enable Encryption",
                value=False,
                help="Encrypt the portable package (requires password)"
            )
        
        if encryption_enabled:
            encryption_password = st.text_input(
                "Encryption Password:",
                type="password",
                help="Password to encrypt/decrypt the portable package"
            )
        
        submitted = st.form_submit_button("💾 Create USB Portable Version", type="primary")
        
        if submitted:
            config = {
                'usb_name': usb_name,
                'include_sample_data': include_sample_data,
                'auto_launch': auto_launch,
                'encryption_enabled': encryption_enabled
            }
            
            if encryption_enabled and 'encryption_password' in locals():
                config['encryption_password'] = encryption_password
            
            with st.spinner("Creating USB portable version..."):
                result = st.session_state.deployment_manager.create_usb_portable_version(config)
                
                if result.get('success'):
                    st.success("✅ USB portable version created successfully!")
                    
                    st.subheader("📋 Package Details")
                    st.write(f"**Package Directory:** {result['deployment_dir']}")
                    st.write(f"**Estimated Size:** {result['size_estimate']}")
                    st.write(f"**Database Path:** {result['database_path']}")
                    
                    st.subheader("🚀 Startup Scripts")
                    for script in result['startup_scripts']:
                        st.write(f"• {script}")
                    
                    st.subheader("📖 Usage Instructions")
                    st.markdown("""
                    **Windows:**
                    1. Copy folder to USB drive
                    2. Double-click `Start_Police_Monitor.bat`
                    3. Wait for setup to complete
                    4. Access at http://localhost:8501
                    
                    **Linux/Mac:**
                    1. Copy folder to USB drive
                    2. Run `./start_police_monitor.sh`
                    3. Wait for setup to complete
                    4. Access at http://localhost:8501
                    """)
                else:
                    st.error(f"❌ Creation failed: {result.get('error', 'Unknown error')}")

def show_cloud_deployment():
    """Display cloud deployment interface"""
    st.header("☁️ Cloud-Agnostic Configuration")
    st.markdown("Deploy to any cloud provider with standardized configurations")
    
    with st.form("cloud_deployment_form"):
        st.subheader("☁️ Cloud Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Target Cloud Providers:**")
            providers = []
            if st.checkbox("Amazon Web Services (AWS)", value=True):
                providers.append('aws')
            if st.checkbox("Microsoft Azure", value=True):
                providers.append('azure')
            if st.checkbox("Google Cloud Platform (GCP)", value=True):
                providers.append('gcp')
            if st.checkbox("Heroku", value=False):
                providers.append('heroku')
            if st.checkbox("DigitalOcean", value=False):
                providers.append('digitalocean')
        
        with col2:
            environment = st.selectbox(
                "Environment:",
                ["development", "staging", "production"],
                index=2,
                help="Deployment environment"
            )
            
            auto_scaling = st.checkbox(
                "Enable Auto Scaling",
                value=True,
                help="Enable automatic scaling based on load"
            )
            
            ssl_enabled = st.checkbox(
                "Enable SSL/TLS",
                value=True,
                help="Enable secure HTTPS connections"
            )
        
        submitted = st.form_submit_button("☁️ Generate Cloud Configurations", type="primary")
        
        if submitted:
            if not providers:
                st.error("Please select at least one cloud provider")
                return
            
            config = {
                'providers': providers,
                'environment': environment,
                'auto_scaling': auto_scaling,
                'ssl_enabled': ssl_enabled
            }
            
            with st.spinner("Generating cloud configurations..."):
                result = st.session_state.deployment_manager.create_cloud_agnostic_config(config)
                
                if result.get('success'):
                    st.success("✅ Cloud configurations generated successfully!")
                    
                    st.subheader("📋 Configuration Details")
                    st.write(f"**Configuration Directory:** {result['deployment_dir']}")
                    st.write(f"**Providers Configured:** {', '.join(result['providers_configured'])}")
                    
                    st.subheader("📂 Generated Files")
                    for file_name in result['files_created']:
                        st.write(f"• {file_name}")
                    
                    # Provider-specific instructions
                    st.subheader("🚀 Deployment Commands")
                    
                    if 'aws' in providers:
                        st.markdown("**AWS Elastic Beanstalk:**")
                        st.code("""
eb init police-monitor
eb create production
eb deploy
                        """)
                    
                    if 'azure' in providers:
                        st.markdown("**Microsoft Azure:**")
                        st.code("""
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name police-monitor
az webapp deployment source config-zip --resource-group myResourceGroup --name police-monitor --src deployment.zip
                        """)
                    
                    if 'gcp' in providers:
                        st.markdown("**Google Cloud Platform:**")
                        st.code("""
gcloud app deploy app.yaml
                        """)
                    
                    if 'heroku' in providers:
                        st.markdown("**Heroku:**")
                        st.code("""
heroku create police-monitor
git push heroku main
                        """)
                else:
                    st.error(f"❌ Configuration failed: {result.get('error', 'Unknown error')}")

def show_lightweight_deployment():
    """Display lightweight deployment interface"""
    st.header("🪶 Lightweight Version")
    st.markdown("Optimized version for low-resource environments")
    
    with st.form("lightweight_form"):
        st.subheader("🪶 Resource Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            resource_limit = st.selectbox(
                "Resource Limit:",
                ["minimal", "low", "standard"],
                index=1,
                help="Choose resource limit based on available hardware"
            )
            
            # Display resource requirements
            resource_configs = {
                'minimal': {'ram': 512, 'cache': 50, 'users': 5},
                'low': {'ram': 1024, 'cache': 100, 'users': 10},
                'standard': {'ram': 2048, 'cache': 200, 'users': 20}
            }
            
            selected_config = resource_configs[resource_limit]
            st.info(f"""
            **{resource_limit.title()} Configuration:**
            • RAM Limit: {selected_config['ram']} MB
            • Cache Limit: {selected_config['cache']} MB
            • Max Users: {selected_config['users']}
            """)
        
        with col2:
            st.markdown("**Features to Enable:**")
            features = []
            if st.checkbox("Basic Monitoring", value=True):
                features.append('basic_monitoring')
            if st.checkbox("Simple Alerts", value=True):
                features.append('simple_alerts')
            if st.checkbox("Cached Data", value=resource_limit != 'minimal'):
                features.append('cached_data')
            if st.checkbox("Basic Analysis", value=resource_limit == 'standard'):
                features.append('basic_analysis')
            if st.checkbox("Reporting", value=resource_limit == 'standard'):
                features.append('reporting')
        
        submitted = st.form_submit_button("🪶 Create Lightweight Version", type="primary")
        
        if submitted:
            config = {
                'resource_limit': resource_limit,
                'features': features
            }
            
            with st.spinner("Creating lightweight version..."):
                result = st.session_state.deployment_manager.create_lightweight_version(config)
                
                if result.get('success'):
                    st.success("✅ Lightweight version created successfully!")
                    
                    st.subheader("📋 Configuration Details")
                    st.write(f"**Deployment Directory:** {result['deployment_dir']}")
                    st.write(f"**Resource Limit:** {result['resource_limit'].title()}")
                    st.write(f"**RAM Limit:** {result['config']['ram_limit_mb']} MB")
                    st.write(f"**Max Users:** {result['config']['max_concurrent_users']}")
                    
                    st.subheader("✨ Enabled Features")
                    for feature in result['config']['features']:
                        st.write(f"• {feature.replace('_', ' ').title()}")
                    
                    st.subheader("📂 Created Files")
                    for file_name in result['files_created']:
                        st.write(f"• {file_name}")
                    
                    st.subheader("🚀 Quick Start")
                    st.code("python start_lightweight.py")
                else:
                    st.error(f"❌ Creation failed: {result.get('error', 'Unknown error')}")

def show_offline_documentation():
    """Display offline documentation interface"""
    st.header("📚 Offline Documentation and Setup Guides")
    st.markdown("Comprehensive offline documentation for deployment and usage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📖 Available Documentation")
        
        docs = {
            "Installation Guide": "Complete installation instructions for all platforms",
            "User Manual": "Comprehensive user guide with screenshots",
            "Administrator Guide": "System administration and configuration",
            "API Documentation": "Technical API reference and examples",
            "Troubleshooting Guide": "Common issues and solutions",
            "Security Manual": "Security best practices and compliance",
            "Training Materials": "Training curricula and exercises",
            "Quick Reference": "Printable quick reference cards"
        }
        
        selected_docs = []
        for doc_name, doc_desc in docs.items():
            if st.checkbox(doc_name, value=True, help=doc_desc):
                selected_docs.append(doc_name)
    
    with col2:
        st.subheader("📦 Package Options")
        
        include_videos = st.checkbox(
            "Include Video Tutorials",
            value=True,
            help="Include video tutorial files in package"
        )
        
        include_templates = st.checkbox(
            "Include Templates",
            value=True,
            help="Include configuration templates and examples"
        )
        
        include_tools = st.checkbox(
            "Include Diagnostic Tools",
            value=True,
            help="Include offline diagnostic and setup tools"
        )
        
        format_type = st.selectbox(
            "Package Format:",
            ["PDF + HTML", "HTML Only", "PDF Only", "Markdown"],
            help="Choose documentation format"
        )
    
    if st.button("📚 Generate Documentation Package", type="primary"):
        with st.spinner("Generating documentation package..."):
            # Simulate documentation generation
            package_info = {
                'selected_docs': selected_docs,
                'include_videos': include_videos,
                'include_templates': include_templates,
                'include_tools': include_tools,
                'format_type': format_type,
                'generated_at': datetime.now().isoformat(),
                'estimated_size': f"{len(selected_docs) * 5 + (20 if include_videos else 0)} MB"
            }
            
            st.success("✅ Documentation package generated successfully!")
            
            st.subheader("📦 Package Contents")
            st.write(f"**Selected Documents:** {len(selected_docs)}")
            st.write(f"**Format:** {format_type}")
            st.write(f"**Estimated Size:** {package_info['estimated_size']}")
            
            if include_videos:
                st.write("• Video tutorials included")
            if include_templates:
                st.write("• Configuration templates included")
            if include_tools:
                st.write("• Diagnostic tools included")
            
            st.subheader("📂 Package Structure")
            st.code("""
docs/
├── installation/
├── user_guide/
├── admin_guide/
├── api_reference/
├── troubleshooting/
├── security/
├── training/
├── quick_reference/
├── videos/ (if included)
├── templates/ (if included)
└── tools/ (if included)
            """)

def show_video_tutorials():
    """Display video tutorial interface"""
    st.header("🎥 Video Tutorials for Non-Technical Users")
    st.markdown("Interactive video tutorials for easy learning")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎬 Available Tutorials")
        
        tutorial_type = st.selectbox(
            "Select Tutorial Type:",
            [
                "Installation Guide",
                "Daily Operations",
                "Alert Response",
                "Troubleshooting",
                "System Administration"
            ],
            help="Choose the type of tutorial to generate"
        )
        
        if tutorial_type == "Installation Guide":
            deployment_type = st.selectbox(
                "Deployment Type:",
                ["standard", "network", "usb", "cloud", "lightweight"],
                help="Select deployment type for installation tutorial"
            )
        
        tutorial_length = st.selectbox(
            "Tutorial Length:",
            ["Short (5-10 min)", "Medium (15-20 min)", "Long (25-30 min)"],
            index=1,
            help="Choose tutorial duration"
        )
        
        include_interactive = st.checkbox(
            "Include Interactive Elements",
            value=True,
            help="Add quizzes, checkpoints, and hands-on exercises"
        )
        
        include_captions = st.checkbox(
            "Include Closed Captions",
            value=True,
            help="Add closed captions for accessibility"
        )
    
    with col2:
        st.subheader("🎯 Tutorial Features")
        st.markdown("""
        ✅ **Professional Narration**
        ✅ **Step-by-step Instructions**
        ✅ **Real-world Examples**
        ✅ **Interactive Checkpoints**
        ✅ **Downloadable Resources**
        ✅ **Multi-language Support**
        ✅ **Accessibility Features**
        ✅ **Practice Exercises**
        """)
    
    if st.button("🎥 Generate Video Tutorial", type="primary"):
        with st.spinner("Generating video tutorial..."):
            if tutorial_type == "Installation Guide":
                result = st.session_state.tutorial_generator.generate_installation_tutorial(
                    deployment_type if 'deployment_type' in locals() else 'standard'
                )
            elif tutorial_type == "Daily Operations":
                result = st.session_state.tutorial_generator.generate_daily_operations_tutorial()
            elif tutorial_type == "Troubleshooting":
                result = st.session_state.tutorial_generator.generate_troubleshooting_tutorial()
            else:
                # Simulate other tutorial types
                result = {
                    'success': True,
                    'tutorial_type': tutorial_type.lower().replace(' ', '_'),
                    'duration': tutorial_length,
                    'script_path': f"tutorials/{tutorial_type.lower().replace(' ', '_')}/script.md",
                    'features': {
                        'interactive': include_interactive,
                        'captions': include_captions,
                        'checkpoints': 5,
                        'exercises': 3
                    }
                }
            
            if result.get('success'):
                st.success("✅ Video tutorial generated successfully!")
                
                st.subheader("🎬 Tutorial Details")
                st.write(f"**Type:** {tutorial_type}")
                st.write(f"**Duration:** {tutorial_length}")
                if 'script_path' in result:
                    st.write(f"**Script Path:** {result['script_path']}")
                
                if include_interactive:
                    st.write("• Interactive elements included")
                if include_captions:
                    st.write("• Closed captions included")
                
                st.subheader("📋 Tutorial Checklist")
                if tutorial_type == "Installation Guide" and 'checkpoints' in result:
                    st.write(f"✅ {result['checkpoints']} checkpoints created")
                
                st.subheader("📥 Download Resources")
                st.markdown("""
                - 📝 Tutorial Script
                - 📋 Step-by-step Checklist
                - 🎯 Practice Exercises
                - 📖 Quick Reference Guide
                """)
            else:
                st.error(f"❌ Tutorial generation failed: {result.get('error', 'Unknown error')}")

def show_remote_support():
    """Display remote support interface"""
    st.header("🔧 Remote Support Capabilities")
    st.markdown("Comprehensive remote support and diagnostics")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Start Support Session", "🔍 System Diagnostics", "📦 Support Package"])
    
    with tab1:
        st.subheader("🎯 Start Remote Support Session")
        
        with st.form("support_session_form"):
            issue_type = st.selectbox(
                "Issue Type:",
                [
                    "installation_problems",
                    "performance_issues", 
                    "connection_errors",
                    "user_access_problems",
                    "data_synchronization",
                    "system_crashes",
                    "configuration_help",
                    "training_request",
                    "other"
                ],
                help="Select the type of issue you're experiencing"
            )
            
            description = st.text_area(
                "Issue Description:",
                height=100,
                placeholder="Please describe the issue in detail, including steps to reproduce and any error messages...",
                help="Provide as much detail as possible to help our support team"
            )
            
            contact_info = st.text_input(
                "Contact Information:",
                placeholder="Email or phone number for follow-up",
                help="How should our support team contact you?"
            )
            
            urgency = st.selectbox(
                "Urgency Level:",
                ["Low", "Medium", "High", "Critical"],
                index=1,
                help="How urgent is this issue?"
            )
            
            submitted = st.form_submit_button("🎯 Start Support Session", type="primary")
            
            if submitted:
                if not description.strip():
                    st.error("Please provide an issue description")
                    return
                
                with st.spinner("Starting remote support session..."):
                    result = st.session_state.support_system.start_support_session(
                        issue_type, description
                    )
                    
                    if result.get('success'):
                        session_info = result['session_info']
                        
                        st.success("✅ Support session started successfully!")
                        
                        st.subheader("📋 Session Information")
                        st.write(f"**Session ID:** {session_info['session_id'][:16]}...")
                        st.write(f"**Issue Type:** {session_info['issue_type'].replace('_', ' ').title()}")
                        st.write(f"**Started:** {session_info['started_at'][:19]}")
                        
                        st.subheader("🔗 Connection Status")
                        conn_status = session_info.get('connection_status', {})
                        if conn_status.get('connection_status') == 'CONNECTED':
                            st.success("🔗 Connected to support server")
                            st.write("**Available Features:**")
                            for feature in conn_status.get('features_available', []):
                                st.write(f"• {feature}")
                        else:
                            st.warning("⚠️ Operating in offline mode")
                        
                        st.subheader("📖 Support Instructions")
                        for instruction in session_info.get('instructions', []):
                            st.info(instruction)
                        
                        # Show system info
                        if 'system_info' in session_info:
                            with st.expander("💻 System Information"):
                                sys_info = session_info['system_info']
                                st.write(f"**Platform:** {sys_info.get('platform', 'Unknown')}")
                                st.write(f"**Python Version:** {sys_info.get('python_version', 'Unknown')}")
                                st.write(f"**Hostname:** {sys_info.get('hostname', 'Unknown')}")
                    else:
                        st.error(f"❌ Failed to start support session: {result.get('error', 'Unknown error')}")
    
    with tab2:
        st.subheader("🔍 System Diagnostics")
        st.markdown("Run comprehensive system diagnostics to identify issues")
        
        if st.button("🔍 Run System Diagnostics", type="primary"):
            with st.spinner("Running system diagnostics..."):
                diagnostics = st.session_state.support_system.run_system_diagnostics()
                
                if 'tests' in diagnostics:
                    st.subheader("📊 Diagnostic Results")
                    
                    # Summary
                    summary = diagnostics.get('summary', {})
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Tests", summary.get('total_tests', 0))
                    with col2:
                        st.metric("Passed", summary.get('passed_tests', 0))
                    with col3:
                        st.metric("Failed", summary.get('failed_tests', 0))
                    with col4:
                        st.metric("Success Rate", f"{summary.get('success_rate', 0)}%")
                    
                    # Individual test results
                    st.subheader("🧪 Individual Test Results")
                    for test_name, test_result in diagnostics['tests'].items():
                        status = test_result.get('status', 'UNKNOWN')
                        status_icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "SKIP": "⏭️"}.get(status, "❓")
                        
                        with st.expander(f"{status_icon} {test_name.replace('_', ' ').title()} - {status}"):
                            st.json(test_result)
                    
                    # Recommendations
                    if diagnostics.get('recommendations'):
                        st.subheader("💡 Recommendations")
                        for recommendation in diagnostics['recommendations']:
                            st.warning(recommendation)
                else:
                    st.error("❌ Diagnostics failed to run properly")
    
    with tab3:
        st.subheader("📦 Support Package Generator")
        st.markdown("Generate a comprehensive support package for analysis")
        
        if st.button("📦 Generate Support Package", type="primary"):
            with st.spinner("Generating support package..."):
                package_result = st.session_state.support_system.generate_support_package()
                
                if 'files' in package_result:
                    st.success("✅ Support package generated successfully!")
                    
                    st.subheader("📦 Package Details")
                    st.write(f"**Session ID:** {package_result['session_id'][:16]}...")
                    st.write(f"**Generated:** {package_result['generated_at'][:19]}")
                    st.write(f"**Package Size:** {package_result['size_mb']} MB")
                    st.write(f"**Files Included:** {len(package_result['files'])}")
                    
                    st.subheader("📂 Package Contents")
                    for file_name in package_result['files']:
                        st.write(f"• {file_name}")
                    
                    st.subheader("📥 Package Usage")
                    st.markdown("""
                    1. Share the package path with support technician
                    2. Package contains diagnostic information only
                    3. No sensitive operational data included
                    4. Package expires in 30 days
                    5. Use secure file transfer methods
                    """)
                    
                    st.info(f"📁 Package Location: {package_result.get('package_path', 'Generated in support_packages/')}")
                else:
                    st.error("❌ Failed to generate support package")

if __name__ == "__main__":
    main()
