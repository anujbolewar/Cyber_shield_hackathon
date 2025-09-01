#!/usr/bin/env python3
"""
Police AI Monitor - Streamlit Cloud Entry Point
Main application file for deployment on Streamlit Cloud
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Set page config first
st.set_page_config(
    page_title="Police AI Monitor - Law Enforcement Intelligence Platform",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Police AI Monitor\nLaw Enforcement Intelligence Platform"
    }
)

def main():
    """Main application entry point for Streamlit Cloud"""
    try:
        # Import and run the main application
        from main import main as run_main_app
        run_main_app()
    except ImportError as e:
        st.error(f"Import error: {e}")
        st.info("Trying alternative import path...")
        try:
            # Alternative import for different deployment environments
            sys.path.insert(0, str(Path(__file__).parent))
            from src.main import main as run_main_app
            run_main_app()
        except Exception as e2:
            st.error(f"Failed to load application: {e2}")
            st.markdown("""
            ## Police AI Monitor
            
            **Law Enforcement Intelligence Platform**
            
            There was an issue loading the main application. This could be due to:
            - Missing dependencies
            - Import path issues
            - Configuration problems
            
            Please check the application logs or contact support.
            """)
            
if __name__ == "__main__":
    main()
