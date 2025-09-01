#!/usr/bin/env python3
"""
🚔 Police AI Monitor - Application Entry Point
Professional entry point for the organized Police AI Monitor system.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main entry point for Police AI Monitor"""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    main_app = project_root / "src" / "main.py"
    
    # Ensure the main app exists
    if not main_app.exists():
        print(f"❌ Error: Main application not found at {main_app}")
        sys.exit(1)
    
    # Print startup message
    print("🚔 Starting Police AI Monitor...")
    print(f"📁 Project root: {project_root}")
    print(f"🎯 Main app: {main_app}")
    print("🚀 Launching Streamlit application...")
    
    # Run Streamlit with the organized structure
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(main_app),
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Police AI Monitor stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
