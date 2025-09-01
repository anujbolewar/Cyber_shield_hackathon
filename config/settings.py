"""
🚔 Police AI Monitor - Configuration Settings
Centralized configuration management for the application.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
DOCS_DIR = PROJECT_ROOT / "docs"
TESTS_DIR = PROJECT_ROOT / "tests"

# Application settings
APP_CONFIG = {
    "title": "🚔 Police AI Monitor",
    "description": "Law Enforcement Social Media Intelligence Platform",
    "version": "1.0.0",
    "author": "Hackathon Team",
    "contact": "police-ai@monitor.com"
}

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": "Police AI Monitor",
    "page_icon": "🚔",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Database configuration
DATABASE_CONFIG = {
    "default_db": DATA_DIR / "police_monitoring.db",
    "backup_interval": 3600,  # 1 hour
    "max_backups": 24
}

# API configuration
API_CONFIG = {
    "rate_limit": 100,  # requests per minute
    "timeout": 30,  # seconds
    "retry_attempts": 3
}

# Security settings
SECURITY_CONFIG = {
    "enable_auth": True,
    "session_timeout": 1800,  # 30 minutes
    "max_login_attempts": 3
}

# Monitoring configuration
MONITORING_CONFIG = {
    "update_interval": 60,  # seconds
    "alert_threshold": 0.8,
    "max_alerts": 100
}

# Visualization settings
VIZ_CONFIG = {
    "theme": "police",
    "color_scheme": ["#1e3a8a", "#3b82f6", "#60a5fa", "#93c5fd"],
    "chart_height": 400
}

# Export settings
EXPORT_CONFIG = {
    "formats": ["json", "csv", "xml", "txt"],
    "max_records": 10000,
    "compression": True
}

def get_config(section=None):
    """Get configuration settings"""
    if section:
        return globals().get(f"{section.upper()}_CONFIG", {})
    
    return {
        "app": APP_CONFIG,
        "streamlit": STREAMLIT_CONFIG,
        "database": DATABASE_CONFIG,
        "api": API_CONFIG,
        "security": SECURITY_CONFIG,
        "monitoring": MONITORING_CONFIG,
        "visualization": VIZ_CONFIG,
        "export": EXPORT_CONFIG
    }
