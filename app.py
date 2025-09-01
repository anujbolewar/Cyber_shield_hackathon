#!/usr/bin/env python3
"""
🚔 Police AI Monitor - Main Application Entry Point
A comprehensive law enforcement social media monitoring and analysis platform.

This is the organized, deployment-ready version of the Police AI Monitor system.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import the main application
from main import main

if __name__ == "__main__":
    main()
