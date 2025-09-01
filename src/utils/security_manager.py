"""
Security Management Module for Police AI Monitor
Handles authentication, API key management, and security monitoring
"""

import streamlit as st
import hashlib
import secrets
import time
from datetime import datetime, timedelta
import json

class SecurityManager:
    """Manages security features for the Police AI Monitor system"""
    
    def __init__(self):
        self.initialize_security_state()
    
    def initialize_security_state(self):
        """Initialize security-related session state variables"""
        if 'security_initialized' not in st.session_state:
            st.session_state.security_initialized = True
            st.session_state.security_level = 'HIGH'
            st.session_state.failed_login_attempts = 0
            st.session_state.last_security_check = datetime.now()
            st.session_state.security_alerts = []
            st.session_state.api_rate_limits = {}
            st.session_state.user_role = 'OFFICER'
            st.session_state.session_timeout = 3600  # 1 hour
            st.session_state.audit_log = []
    
    def check_session_timeout(self):
        """Check if user session has timed out"""
        if 'last_activity' in st.session_state:
            if datetime.now() - st.session_state.last_activity > timedelta(seconds=st.session_state.session_timeout):
                self.force_logout("Session timeout")
                return False
        st.session_state.last_activity = datetime.now()
        return True
    
    def force_logout(self, reason="Security measure"):
        """Force user logout and clear sensitive data"""
        self.log_security_event(f"Forced logout: {reason}")
        # Clear sensitive session data
        for key in ['api_keys', 'user_authenticated', 'current_user']:
            if key in st.session_state:
                del st.session_state[key]
        st.error(f"🔒 Session terminated: {reason}")
        st.stop()
    
    def validate_api_key(self, api_key, platform):
        """Validate API key format and add rate limiting"""
        if not api_key or len(api_key) < 10:
            return False, "Invalid API key format"
        
        # Check rate limits
        current_time = time.time()
        if platform in st.session_state.api_rate_limits:
            last_check = st.session_state.api_rate_limits[platform]
            if current_time - last_check < 1:  # 1 second rate limit
                return False, "Rate limit exceeded"
        
        st.session_state.api_rate_limits[platform] = current_time
        return True, "API key valid"
    
    def encrypt_api_key(self, api_key):
        """Simple encryption for API keys (in production, use proper encryption)"""
        return hashlib.sha256(api_key.encode()).hexdigest()[:16] + "..."
    
    def generate_security_token(self):
        """Generate a secure token for session management"""
        return secrets.token_urlsafe(32)
    
    def log_security_event(self, event, severity="INFO"):
        """Log security-related events"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "severity": severity,
            "user": st.session_state.get('current_user', 'Unknown'),
            "ip": "127.0.0.1"  # In production, get real IP
        }
        
        if 'audit_log' not in st.session_state:
            st.session_state.audit_log = []
        
        st.session_state.audit_log.append(log_entry)
        
        # Keep only last 100 entries
        if len(st.session_state.audit_log) > 100:
            st.session_state.audit_log = st.session_state.audit_log[-100:]
    
    def check_security_threats(self):
        """Monitor for potential security threats"""
        threats = []
        
        # Check failed login attempts
        if st.session_state.failed_login_attempts > 3:
            threats.append("Multiple failed login attempts detected")
        
        # Check for suspicious API usage
        current_time = time.time()
        for platform, last_check in st.session_state.api_rate_limits.items():
            if current_time - last_check < 0.1:  # Very frequent API calls
                threats.append(f"Suspicious API activity on {platform}")
        
        # Check session duration
        if 'session_start' in st.session_state:
            session_duration = datetime.now() - st.session_state.session_start
            if session_duration > timedelta(hours=8):
                threats.append("Extended session duration detected")
        
        return threats
    
    def display_security_dashboard(self):
        """Display security status dashboard"""
        st.subheader("🔒 Security Status Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            security_score = max(0, 100 - st.session_state.failed_login_attempts * 10)
            st.metric("Security Score", f"{security_score}%", 
                     delta=None if security_score > 80 else "⚠️ Low")
        
        with col2:
            active_sessions = 1  # Current session
            st.metric("Active Sessions", active_sessions)
        
        with col3:
            threat_count = len(self.check_security_threats())
            st.metric("Threat Alerts", threat_count, 
                     delta="🔴 High" if threat_count > 2 else None)
        
        with col4:
            last_check = st.session_state.last_security_check
            time_since = datetime.now() - last_check
            st.metric("Last Security Check", f"{time_since.seconds}s ago")
        
        # Security alerts
        threats = self.check_security_threats()
        if threats:
            st.error("🚨 Security Alerts:")
            for threat in threats:
                st.write(f"• {threat}")
        else:
            st.success("✅ No security threats detected")
    
    def display_audit_log(self, limit=10):
        """Display recent audit log entries"""
        st.subheader("📋 Security Audit Log")
        
        if 'audit_log' not in st.session_state or not st.session_state.audit_log:
            st.info("No audit log entries found")
            return
        
        recent_logs = st.session_state.audit_log[-limit:]
        
        for log_entry in reversed(recent_logs):
            severity_color = {
                "INFO": "🟢",
                "WARNING": "🟡", 
                "ERROR": "🔴",
                "CRITICAL": "🚨"
            }.get(log_entry["severity"], "⚪")
            
            with st.expander(f"{severity_color} {log_entry['timestamp']} - {log_entry['event'][:50]}..."):
                st.json(log_entry)
    
    def require_authentication(self, required_role=None):
        """Require user authentication with optional role check"""
        if not st.session_state.get('user_authenticated', False):
            self.display_login_form()
            st.stop()
        
        if required_role and st.session_state.get('user_role') != required_role:
            st.error(f"❌ Access Denied - Required role: {required_role}")
            st.stop()
        
        # Check session timeout
        if not self.check_session_timeout():
            st.stop()
    
    def display_login_form(self):
        """Display login form for authentication"""
        st.title("🔐 Police AI Monitor - Secure Login")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h2>🚓 AUTHORIZED PERSONNEL ONLY</h2>
            <p>This system is for official law enforcement use only</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.subheader("Enter Credentials")
            
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            badge_number = st.text_input("🎖️ Badge Number")
            
            if st.form_submit_button("🔓 Login"):
                if self.authenticate_user(username, password, badge_number):
                    st.success("✅ Authentication successful")
                    st.session_state.user_authenticated = True
                    st.session_state.current_user = username
                    st.session_state.session_start = datetime.now()
                    self.log_security_event(f"User {username} logged in successfully")
                    st.rerun()
                else:
                    st.session_state.failed_login_attempts += 1
                    self.log_security_event(f"Failed login attempt for {username}", "WARNING")
                    st.error("❌ Invalid credentials")
    
    def authenticate_user(self, username, password, badge_number):
        """Authenticate user credentials (simplified for demo)"""
        # In production, this would connect to a secure authentication system
        valid_users = {
            "officer1": {"password": "secure123", "badge": "B001", "role": "OFFICER"},
            "detective1": {"password": "detective456", "badge": "D001", "role": "DETECTIVE"},
            "admin": {"password": "admin789", "badge": "A001", "role": "ADMIN"}
        }
        
        if username in valid_users:
            user_data = valid_users[username]
            if (password == user_data["password"] and 
                badge_number == user_data["badge"]):
                st.session_state.user_role = user_data["role"]
                return True
        
        return False
    
    def display_security_settings(self):
        """Display security configuration settings"""
        st.subheader("⚙️ Security Settings")
        
        # Security level
        security_level = st.selectbox(
            "Security Level",
            ["LOW", "MEDIUM", "HIGH", "MAXIMUM"],
            index=2,
            help="Higher levels enable additional security measures"
        )
        st.session_state.security_level = security_level
        
        # Session timeout
        timeout_minutes = st.slider(
            "Session Timeout (minutes)",
            min_value=15,
            max_value=480,
            value=60,
            help="Automatic logout after inactivity"
        )
        st.session_state.session_timeout = timeout_minutes * 60
        
        # Two-factor authentication
        enable_2fa = st.checkbox("Enable Two-Factor Authentication", value=True)
        
        # Audit logging
        enable_audit = st.checkbox("Enable Detailed Audit Logging", value=True)
        
        # API rate limiting
        enable_rate_limit = st.checkbox("Enable API Rate Limiting", value=True)
        
        if st.button("💾 Save Security Settings"):
            self.log_security_event("Security settings updated")
            st.success("Security settings saved successfully")
    
    def get_security_status(self):
        """Get current security status"""
        threats = self.check_security_threats()
        
        if threats:
            return "COMPROMISED", threats
        elif st.session_state.security_level == "MAXIMUM":
            return "SECURE", []
        elif st.session_state.security_level == "HIGH":
            return "PROTECTED", []
        else:
            return "BASIC", []

# Global security manager instance
security_manager = SecurityManager()
