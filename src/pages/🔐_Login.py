#!/usr/bin/env python3
"""
🔐 AUTHENTICATION SYSTEM - POLICE AI MONITORING
Secure authentication for law enforcement access
"""

import streamlit as st
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="Police AI Monitor - Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for Police Authentication
st.markdown("""
<style>
    /* Police Authentication Theme */
    :root {
        --police-blue: #1e3a8a;
        --police-blue-dark: #1e40af;
        --police-blue-light: #3b82f6;
        --police-accent: #fbbf24;
        --police-red: #dc2626;
        --police-green: #16a34a;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Login container */
    .login-container {
        background: linear-gradient(135deg, var(--police-blue) 0%, var(--police-blue-dark) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--police-red) 0%, var(--police-accent) 50%, var(--police-green) 100%);
    }
    
    .login-header {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .login-subtitle {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Login form styling */
    .login-form {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid transparent !important;
        border-radius: 8px !important;
        color: var(--police-blue) !important;
        font-weight: 500 !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--police-accent) !important;
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--police-accent) 0%, #f59e0b 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #f59e0b 0%, var(--police-accent) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(251, 191, 36, 0.4) !important;
    }
    
    /* Security badges */
    .security-badge {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        display: inline-block;
        font-size: 14px;
    }
    
    /* Success message */
    .success-login {
        background: linear-gradient(135deg, var(--police-green) 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
    }
    
    /* Error message */
    .error-login {
        background: linear-gradient(135deg, var(--police-red) 0%, #b91c1c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
    }
    
    /* Footer */
    .auth-footer {
        text-align: center;
        color: #64748b;
        margin-top: 2rem;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Predefined users (in production, this would be from a secure database)
AUTHORIZED_USERS = {
    "admin": {
        "password": "admin123",  # In production, this would be hashed
        "name": "Administrator",
        "badge": "ADMIN-001",
        "department": "System Administration",
        "clearance": "TOP_SECRET"
    },
    "officer.johnson": {
        "password": "police123",
        "name": "Officer Johnson",
        "badge": "PD-2024-001",
        "department": "Intelligence Division",
        "clearance": "SECRET"
    },
    "detective.smith": {
        "password": "detective123",
        "name": "Detective Smith",
        "badge": "DT-2024-005",
        "department": "Criminal Investigation",
        "clearance": "SECRET"
    },
    "analyst.davis": {
        "password": "analyst123",
        "name": "Analyst Davis",
        "badge": "AN-2024-012",
        "department": "Intelligence Analysis",
        "clearance": "CONFIDENTIAL"
    }
}

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username: str, password: str) -> tuple:
    """Verify user credentials"""
    if username in AUTHORIZED_USERS:
        stored_password = AUTHORIZED_USERS[username]["password"]
        if password == stored_password:  # In production, compare hashes
            return True, AUTHORIZED_USERS[username]
    return False, None

def create_session(user_data: dict):
    """Create authenticated session"""
    st.session_state.user_authenticated = True
    st.session_state.current_user = user_data
    st.session_state.login_time = datetime.now()
    st.session_state.session_timeout = datetime.now() + timedelta(hours=8)

def check_session_timeout():
    """Check if session has expired"""
    if 'session_timeout' in st.session_state:
        if datetime.now() > st.session_state.session_timeout:
            st.session_state.user_authenticated = False
            return True
    return False

def logout():
    """Logout and clear session"""
    st.session_state.user_authenticated = False
    if 'current_user' in st.session_state:
        del st.session_state.current_user
    if 'login_time' in st.session_state:
        del st.session_state.login_time
    if 'session_timeout' in st.session_state:
        del st.session_state.session_timeout

def display_login_form():
    """Display the login form"""
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            🔐 POLICE AI MONITORING SYSTEM
        </div>
        <div class="login-subtitle">
            Secure Access Portal for Law Enforcement Operations
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.container():
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔑 Officer Login")
            
            # Username input
            username = st.text_input(
                "👤 Username / Badge ID",
                placeholder="Enter your username or badge ID",
                key="login_username"
            )
            
            # Password input
            password = st.text_input(
                "🔒 Password", 
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            # Login button
            if st.button("🚔 Access System", key="login_btn"):
                if username and password:
                    with st.spinner("🔍 Verifying credentials..."):
                        time.sleep(1)  # Simulate authentication delay
                        
                        is_valid, user_data = verify_credentials(username, password)
                        
                        if is_valid:
                            create_session(user_data)
                            st.markdown("""
                            <div class="success-login">
                                ✅ Authentication Successful!<br>
                                Redirecting to dashboard...
                            </div>
                            """, unsafe_allow_html=True)
                            
                            time.sleep(2)
                            st.switch_page("pages/0_🏠_Dashboard.py")
                        else:
                            st.markdown("""
                            <div class="error-login">
                                ❌ Invalid Credentials<br>
                                Access denied. Please check your username and password.
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Demo credentials
    st.markdown("---")
    st.markdown("### 🧪 Demo Credentials")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **👤 Administrator Access:**
        - Username: `admin`
        - Password: `admin123`
        - Clearance: TOP SECRET
        """)
        
        st.markdown("""
        **👮 Officer Access:**
        - Username: `officer.johnson`
        - Password: `police123`
        - Clearance: SECRET
        """)
    
    with col2:
        st.markdown("""
        **🕵️ Detective Access:**
        - Username: `detective.smith`
        - Password: `detective123`
        - Clearance: SECRET
        """)
        
        st.markdown("""
        **📊 Analyst Access:**
        - Username: `analyst.davis`
        - Password: `analyst123`
        - Clearance: CONFIDENTIAL
        """)
    
    # Security features
    st.markdown("### 🛡️ Security Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="security-badge">
            🔐 Encrypted Authentication
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="security-badge">
            ⏰ Session Timeout (8 hours)
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="security-badge">
            🚔 Role-based Access Control
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="auth-footer">
        <p><strong>Police AI Monitoring System</strong> | Secure Law Enforcement Portal</p>
        <p>🔒 All access attempts are logged and monitored</p>
        <p>For technical support, contact IT Security Division</p>
    </div>
    """, unsafe_allow_html=True)

def display_logout_option():
    """Display logout option for authenticated users"""
    if st.session_state.get('user_authenticated', False):
        user = st.session_state.current_user
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"### 👮 {user['name']}")
        st.sidebar.markdown(f"**Badge:** {user['badge']}")
        st.sidebar.markdown(f"**Department:** {user['department']}")
        st.sidebar.markdown(f"**Clearance:** {user['clearance']}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

def main():
    """Main authentication application"""
    # Check for existing authentication
    if st.session_state.get('user_authenticated', False):
        # Check session timeout
        if check_session_timeout():
            st.error("🕐 Session expired. Please login again.")
            logout()
            st.rerun()
        else:
            # Already authenticated, redirect to dashboard
            st.success("✅ Already authenticated. Redirecting to dashboard...")
            time.sleep(1)
            st.switch_page("pages/0_🏠_Dashboard.py")
    else:
        # Display login form
        display_login_form()
    
    # Display logout option in sidebar if authenticated
    display_logout_option()

if __name__ == "__main__":
    main()
