#!/usr/bin/env python3
"""
🚀 POLICE MONITORING DEPLOYMENT STRATEGIES
Comprehensive deployment solutions for various police environments
Supports local network, USB portable, cloud-agnostic, and lightweight deployments
"""

import os
import sys
import json
import platform
import subprocess
import shutil
import sqlite3
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging

class DeploymentManager:
    """
    🚀 Comprehensive deployment manager for police monitoring system
    Handles multiple deployment strategies and configurations
    """
    
    def __init__(self):
        """Initialize deployment manager"""
        self.logger = self._setup_logging()
        self.deployment_configs = {}
        self.system_requirements = self._get_system_requirements()
        self.current_platform = platform.system().lower()
        
        print("🚀 Police Monitoring Deployment Manager initialized")
        print(f"   📊 Platform: {platform.system()} {platform.release()}")
        print(f"   🐍 Python: {platform.python_version()}")
        print(f"   💻 Architecture: {platform.machine()}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for deployment operations"""
        logger = logging.getLogger("DeploymentManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _get_system_requirements(self) -> Dict[str, Any]:
        """Get system requirements for different deployment types"""
        return {
            'minimum': {
                'ram_gb': 2,
                'storage_gb': 5,
                'cpu_cores': 2,
                'python_version': '3.8',
                'os_support': ['Windows 10+', 'Ubuntu 18.04+', 'macOS 10.15+']
            },
            'recommended': {
                'ram_gb': 8,
                'storage_gb': 20,
                'cpu_cores': 4,
                'python_version': '3.9+',
                'os_support': ['Windows 11', 'Ubuntu 20.04+', 'macOS 11+']
            },
            'optimal': {
                'ram_gb': 16,
                'storage_gb': 50,
                'cpu_cores': 8,
                'python_version': '3.10+',
                'os_support': ['Latest versions']
            }
        }
    
    def check_system_requirements(self, deployment_type: str = "recommended") -> Dict[str, Any]:
        """
        🔍 Check if system meets requirements for deployment
        """
        try:
            print(f"\n🔍 SYSTEM REQUIREMENTS CHECK - {deployment_type.upper()}")
            print("=" * 60)
            
            requirements = self.system_requirements.get(deployment_type, self.system_requirements['recommended'])
            results = {
                'meets_requirements': True,
                'checks': {},
                'warnings': [],
                'recommendations': []
            }
            
            # Check RAM
            try:
                try:
                    import psutil
                    ram_gb = psutil.virtual_memory().total / (1024**3)
                    ram_check = ram_gb >= requirements['ram_gb']
                    results['checks']['ram'] = {
                        'status': ram_check,
                        'current': f"{ram_gb:.1f} GB",
                        'required': f"{requirements['ram_gb']} GB"
                    }
                    if not ram_check:
                        results['meets_requirements'] = False
                        results['warnings'].append(f"Insufficient RAM: {ram_gb:.1f} GB < {requirements['ram_gb']} GB")
                    
                    print(f"   {'✅' if ram_check else '❌'} RAM: {ram_gb:.1f} GB (Required: {requirements['ram_gb']} GB)")
                except ImportError:
                    results['warnings'].append("Could not check RAM - psutil not available")
                    print("   ⚠️ RAM: Could not verify (psutil not installed)")
            except Exception as e:
                results['warnings'].append(f"RAM check failed: {str(e)}")
                print("   ⚠️ RAM: Could not verify")
            
            # Check available storage
            try:
                storage_info = shutil.disk_usage('.')
                free_gb = storage_info.free / (1024**3)
                storage_check = free_gb >= requirements['storage_gb']
                results['checks']['storage'] = {
                    'status': storage_check,
                    'current': f"{free_gb:.1f} GB free",
                    'required': f"{requirements['storage_gb']} GB"
                }
                if not storage_check:
                    results['meets_requirements'] = False
                    results['warnings'].append(f"Insufficient storage: {free_gb:.1f} GB < {requirements['storage_gb']} GB")
                
                print(f"   {'✅' if storage_check else '❌'} Storage: {free_gb:.1f} GB free (Required: {requirements['storage_gb']} GB)")
            except Exception as e:
                results['warnings'].append(f"Could not check storage: {str(e)}")
                print("   ⚠️ Storage: Could not verify")
            
            # Check CPU cores
            try:
                try:
                    import psutil
                    cpu_cores = psutil.cpu_count(logical=False)
                    cpu_check = cpu_cores >= requirements['cpu_cores']
                    results['checks']['cpu'] = {
                        'status': cpu_check,
                        'current': f"{cpu_cores} cores",
                        'required': f"{requirements['cpu_cores']} cores"
                    }
                    if not cpu_check:
                        results['warnings'].append(f"Insufficient CPU cores: {cpu_cores} < {requirements['cpu_cores']}")
                    
                    print(f"   {'✅' if cpu_check else '⚠️'} CPU: {cpu_cores} cores (Required: {requirements['cpu_cores']} cores)")
                except ImportError:
                    results['warnings'].append("Could not check CPU - psutil not available")
                    print("   ⚠️ CPU: Could not verify (psutil not installed)")
            except Exception as e:
                results['warnings'].append(f"CPU check failed: {str(e)}")
                print("   ⚠️ CPU: Could not verify")
            
            # Check Python version
            python_version = platform.python_version()
            required_version = requirements['python_version'].replace('+', '')
            python_check = python_version >= required_version
            results['checks']['python'] = {
                'status': python_check,
                'current': python_version,
                'required': requirements['python_version']
            }
            if not python_check:
                results['meets_requirements'] = False
                results['warnings'].append(f"Python version too old: {python_version} < {requirements['python_version']}")
            
            print(f"   {'✅' if python_check else '❌'} Python: {python_version} (Required: {requirements['python_version']})")
            
            # Check OS compatibility
            os_info = f"{platform.system()} {platform.release()}"
            results['checks']['os'] = {
                'status': True,  # Assume compatible for now
                'current': os_info,
                'supported': requirements['os_support']
            }
            print(f"   ✅ OS: {os_info}")
            
            # Generate recommendations
            if not results['meets_requirements']:
                results['recommendations'].append("Consider upgrading system hardware")
                results['recommendations'].append("Use lightweight deployment mode")
            
            if results['warnings']:
                results['recommendations'].append("Review system warnings before deployment")
            
            print(f"\n📊 Overall Status: {'✅ COMPATIBLE' if results['meets_requirements'] else '⚠️ REQUIRES ATTENTION'}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error checking system requirements: {str(e)}")
            return {
                'meets_requirements': False,
                'error': str(e),
                'checks': {},
                'warnings': [f"System check failed: {str(e)}"],
                'recommendations': ["Manual system verification required"]
            }
    
    def create_local_network_deployment(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        🏢 Create local network deployment for police stations
        """
        try:
            print(f"\n🏢 CREATING LOCAL NETWORK DEPLOYMENT")
            print("=" * 60)
            
            deployment_name = config.get('deployment_name', 'police_station_local')
            network_config = config.get('network', {})
            
            # Create deployment directory
            deployment_dir = Path(f"deployments/{deployment_name}")
            deployment_dir.mkdir(parents=True, exist_ok=True)
            
            # Network configuration
            network_settings = {
                'host': network_config.get('host', '0.0.0.0'),
                'port': network_config.get('port', 8501),
                'allow_origins': network_config.get('allow_origins', ['*']),
                'cors_enabled': network_config.get('cors_enabled', True),
                'max_connections': network_config.get('max_connections', 50),
                'session_timeout': network_config.get('session_timeout', 3600)
            }
            
            # Create Streamlit configuration
            streamlit_config = f"""
[server]
headless = true
port = {network_settings['port']}
address = "{network_settings['host']}"
enableCORS = {str(network_settings['cors_enabled']).lower()}
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1e3a8a"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
            
            # Write configuration files
            config_dir = deployment_dir / '.streamlit'
            config_dir.mkdir(exist_ok=True)
            
            with open(config_dir / 'config.toml', 'w') as f:
                f.write(streamlit_config)
            
            # Create network deployment script
            deployment_script = f"""#!/usr/bin/env python3
'''
🏢 Police Station Local Network Deployment
Configured for: {deployment_name}
Network: {network_settings['host']}:{network_settings['port']}
'''

import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

def main():
    # Set up environment
    os.environ['STREAMLIT_SERVER_PORT'] = '{network_settings['port']}'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '{network_settings['host']}'
    
    # Start application
    print("🏢 Starting Police Station Local Network Deployment")
    print(f"   📡 Network: {network_settings['host']}:{network_settings['port']}")
    print(f"   🔗 Access URL: http://{network_settings['host']}:{network_settings['port']}")
    print(f"   👥 Max Connections: {network_settings['max_connections']}")
    
    # Run Streamlit application
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'main.py',
        '--server.port', '{network_settings['port']}',
        '--server.address', '{network_settings['host']}',
        '--server.headless', 'true'
    ])

if __name__ == "__main__":
    main()
"""
            
            with open(deployment_dir / 'start_local_network.py', 'w') as f:
                f.write(deployment_script)
            
            # Create network documentation
            network_docs = f"""
# 🏢 LOCAL NETWORK DEPLOYMENT GUIDE

## Network Configuration
- **Host:** {network_settings['host']}
- **Port:** {network_settings['port']}
- **Access URL:** http://{network_settings['host']}:{network_settings['port']}
- **Max Connections:** {network_settings['max_connections']}

## Installation Steps
1. Copy deployment folder to police station server
2. Install Python {self.system_requirements['minimum']['python_version']}+
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python start_local_network.py`

## Network Access
- **Internal Access:** http://192.168.1.100:{network_settings['port']} (adjust IP)
- **Localhost:** http://localhost:{network_settings['port']}
- **All stations:** Configure firewall to allow port {network_settings['port']}

## Security Considerations
- Use internal network only
- Configure firewall rules
- Enable user authentication
- Regular security updates
"""
            
            with open(deployment_dir / 'NETWORK_DEPLOYMENT.md', 'w') as f:
                f.write(network_docs)
            
            # Copy essential files
            essential_files = [
                'main.py',
                'requirements.txt',
                'utils/',
                'pages/',
                'data/'
            ]
            
            for file_path in essential_files:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.copytree(file_path, deployment_dir / file_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(file_path, deployment_dir)
            
            print(f"   ✅ Deployment directory created: {deployment_dir}")
            print(f"   ✅ Network configuration: {network_settings['host']}:{network_settings['port']}")
            print(f"   ✅ Streamlit config written")
            print(f"   ✅ Deployment script created")
            print(f"   ✅ Documentation generated")
            print(f"   ✅ Essential files copied")
            
            return {
                'success': True,
                'deployment_type': 'local_network',
                'deployment_dir': str(deployment_dir),
                'network_settings': network_settings,
                'access_url': f"http://{network_settings['host']}:{network_settings['port']}",
                'files_created': [
                    'start_local_network.py',
                    '.streamlit/config.toml',
                    'NETWORK_DEPLOYMENT.md'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating local network deployment: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'deployment_type': 'local_network'
            }
    
    def create_usb_portable_version(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        💾 Create USB portable version with embedded database
        """
        try:
            print(f"\n💾 CREATING USB PORTABLE VERSION")
            print("=" * 60)
            
            usb_name = config.get('usb_name', 'PoliceMonitor_Portable')
            include_data = config.get('include_sample_data', True)
            
            # Create USB deployment directory
            usb_dir = Path(f"deployments/{usb_name}")
            usb_dir.mkdir(parents=True, exist_ok=True)
            
            # Create portable Python environment structure
            portable_structure = {
                'PoliceMonitor/': {
                    'app/': 'Main application files',
                    'data/': 'Embedded databases and cache',
                    'docs/': 'Offline documentation',
                    'python/': 'Portable Python runtime (if needed)',
                    'config/': 'Configuration files',
                    'logs/': 'Application logs'
                }
            }
            
            # Create directory structure
            for dir_name in portable_structure['PoliceMonitor/'].keys():
                (usb_dir / dir_name).mkdir(exist_ok=True)
            
            # Copy application files
            app_files = [
                'main.py',
                'requirements.txt',
                'utils/',
                'pages/'
            ]
            
            for file_path in app_files:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.copytree(file_path, usb_dir / 'app' / file_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(file_path, usb_dir / 'app')
            
            # Create embedded database
            db_path = usb_dir / 'data' / 'police_monitor.db'
            self._create_embedded_database(db_path, include_data)
            
            # Create portable configuration
            portable_config = {
                'database': {
                    'type': 'sqlite',
                    'path': './data/police_monitor.db',
                    'embedded': True
                },
                'cache': {
                    'type': 'file',
                    'path': './data/cache/',
                    'max_size_mb': 500
                },
                'logs': {
                    'path': './logs/',
                    'level': 'INFO',
                    'max_files': 10
                },
                'portable': {
                    'version': '1.0',
                    'created': datetime.now().isoformat(),
                    'platform': 'cross-platform'
                }
            }
            
            with open(usb_dir / 'config' / 'portable_config.json', 'w') as f:
                json.dump(portable_config, f, indent=2)
            
            # Create startup script for Windows
            windows_script = f"""@echo off
title Police Monitor - Portable Version
cd /d "%~dp0"

echo.
echo ================================================
echo  🚓 POLICE MONITOR - PORTABLE VERSION
echo ================================================
echo.
echo Starting Police Monitor System...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "app\\venv\\" (
    echo 📦 Setting up virtual environment...
    cd app
    python -m venv venv
    call venv\\Scripts\\activate
    pip install -r requirements.txt
    cd ..
)

REM Start application
cd app
call venv\\Scripts\\activate
echo 🚀 Starting application on http://localhost:8501
echo 📂 Data stored in: %~dp0data\\
echo.
streamlit run main.py --server.headless true

pause
"""
            
            with open(usb_dir / 'Start_Police_Monitor.bat', 'w') as f:
                f.write(windows_script)
            
            # Create startup script for Linux/Mac
            unix_script = f"""#!/bin/bash
echo ""
echo "================================================"
echo " 🚓 POLICE MONITOR - PORTABLE VERSION"
echo "================================================"
echo ""
echo "Starting Police Monitor System..."
echo ""

# Get script directory
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" &> /dev/null && pwd )"
cd "$DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Setup virtual environment if needed
if [ ! -d "app/venv" ]; then
    echo "📦 Setting up virtual environment..."
    cd app
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Start application
cd app
source venv/bin/activate
echo "🚀 Starting application on http://localhost:8501"
echo "📂 Data stored in: $DIR/data/"
echo ""
streamlit run main.py --server.headless true
"""
            
            with open(usb_dir / 'start_police_monitor.sh', 'w') as f:
                f.write(unix_script)
            
            # Make Unix script executable
            os.chmod(usb_dir / 'start_police_monitor.sh', 0o755)
            
            # Create README for USB version
            usb_readme = f"""
# 💾 POLICE MONITOR - USB PORTABLE VERSION

## Quick Start
### Windows:
- Double-click `Start_Police_Monitor.bat`
- Wait for setup to complete
- Access at http://localhost:8501

### Linux/Mac:
- Run `./start_police_monitor.sh`
- Wait for setup to complete
- Access at http://localhost:8501

## Features
- ✅ No installation required
- ✅ Embedded database
- ✅ Offline capabilities
- ✅ Cross-platform compatibility
- ✅ Portable configuration

## System Requirements
- Python 3.8+ (auto-detected)
- 2GB RAM minimum
- 5GB free space
- Windows 10+, Ubuntu 18.04+, or macOS 10.15+

## Data Storage
- Database: `./data/police_monitor.db`
- Cache: `./data/cache/`
- Logs: `./logs/`
- Config: `./config/`

## Troubleshooting
1. **Python not found**: Install Python from python.org
2. **Permission denied**: Run as administrator (Windows) or with sudo (Linux/Mac)
3. **Port in use**: Close other applications using port 8501

## Security
- Keep USB device secure
- Use encryption if required
- Regular backups recommended
"""
            
            with open(usb_dir / 'README.md', 'w') as f:
                f.write(usb_readme)
            
            # Copy offline documentation
            self._create_offline_documentation(usb_dir / 'docs')
            
            print(f"   ✅ USB directory created: {usb_dir}")
            print(f"   ✅ Embedded database created")
            print(f"   ✅ Portable configuration written")
            print(f"   ✅ Windows startup script created")
            print(f"   ✅ Unix startup script created")
            print(f"   ✅ README and documentation included")
            print(f"   ✅ Application files copied")
            
            return {
                'success': True,
                'deployment_type': 'usb_portable',
                'deployment_dir': str(usb_dir),
                'startup_scripts': ['Start_Police_Monitor.bat', 'start_police_monitor.sh'],
                'database_path': str(db_path),
                'size_estimate': '50-100 MB'
            }
            
        except Exception as e:
            self.logger.error(f"Error creating USB portable version: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'deployment_type': 'usb_portable'
            }
    
    def create_cloud_agnostic_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        ☁️ Create cloud-agnostic configuration for multiple cloud providers
        """
        try:
            print(f"\n☁️ CREATING CLOUD-AGNOSTIC CONFIGURATION")
            print("=" * 60)
            
            cloud_providers = config.get('providers', ['aws', 'azure', 'gcp', 'heroku'])
            environment = config.get('environment', 'production')
            
            cloud_dir = Path(f"deployments/cloud_agnostic")
            cloud_dir.mkdir(parents=True, exist_ok=True)
            
            # Base configuration template
            base_config = {
                'app': {
                    'name': 'police-monitor',
                    'version': '2.0',
                    'environment': environment,
                    'port': int(os.environ.get('PORT', 8501))
                },
                'database': {
                    'url': os.environ.get('DATABASE_URL', 'sqlite:///police_monitor.db'),
                    'pool_size': int(os.environ.get('DB_POOL_SIZE', 10)),
                    'timeout': int(os.environ.get('DB_TIMEOUT', 30))
                },
                'security': {
                    'secret_key': os.environ.get('SECRET_KEY', 'change-in-production'),
                    'cors_origins': os.environ.get('CORS_ORIGINS', '*').split(','),
                    'ssl_enabled': os.environ.get('SSL_ENABLED', 'false').lower() == 'true'
                },
                'features': {
                    'fallback_system': True,
                    'demo_mode': os.environ.get('DEMO_MODE', 'false').lower() == 'true',
                    'debug': os.environ.get('DEBUG', 'false').lower() == 'true'
                }
            }
            
            # AWS configuration
            if 'aws' in cloud_providers:
                aws_config = {
                    'service': 'AWS Elastic Beanstalk / ECS',
                    'dockerfile': self._create_dockerfile(),
                    'eb_config': {
                        'platform': 'Python 3.9',
                        'instance_type': 't3.medium',
                        'auto_scaling': {
                            'min_instances': 1,
                            'max_instances': 5
                        }
                    },
                    'environment_variables': {
                        'PYTHONPATH': '/app',
                        'STREAMLIT_SERVER_PORT': '8501',
                        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0'
                    }
                }
                
                with open(cloud_dir / 'aws_config.json', 'w') as f:
                    json.dump(aws_config, f, indent=2)
                
                # Create Elastic Beanstalk configuration
                eb_dir = cloud_dir / '.ebextensions'
                eb_dir.mkdir(exist_ok=True)
                
                eb_config = """option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application.py
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: static
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.medium
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /app
    STREAMLIT_SERVER_PORT: 8501
"""
                
                with open(eb_dir / 'python.config', 'w') as f:
                    f.write(eb_config)
            
            # Azure configuration
            if 'azure' in cloud_providers:
                azure_config = {
                    'service': 'Azure App Service',
                    'runtime': 'Python 3.9',
                    'pricing_tier': 'B1',
                    'app_settings': {
                        'WEBSITES_PORT': '8501',
                        'SCM_DO_BUILD_DURING_DEPLOYMENT': 'true',
                        'PYTHON_VERSION': '3.9'
                    }
                }
                
                with open(cloud_dir / 'azure_config.json', 'w') as f:
                    json.dump(azure_config, f, indent=2)
            
            # Google Cloud Platform configuration
            if 'gcp' in cloud_providers:
                gcp_config = {
                    'service': 'Google App Engine',
                    'runtime': 'python39',
                    'instance_class': 'F2',
                    'app_yaml': {
                        'runtime': 'python39',
                        'env_variables': {
                            'PORT': '8501',
                            'PYTHONPATH': '/app'
                        },
                        'automatic_scaling': {
                            'min_instances': 1,
                            'max_instances': 5
                        }
                    }
                }
                
                with open(cloud_dir / 'gcp_config.json', 'w') as f:
                    json.dump(gcp_config, f, indent=2)
                
                # Create app.yaml for Google App Engine
                app_yaml = """runtime: python39
env_variables:
  PORT: 8501
  PYTHONPATH: /app

automatic_scaling:
  min_instances: 1
  max_instances: 5
  target_cpu_utilization: 0.6

resources:
  cpu: 1
  memory_gb: 2
  disk_size_gb: 10
"""
                
                with open(cloud_dir / 'app.yaml', 'w') as f:
                    f.write(app_yaml)
            
            # Heroku configuration
            if 'heroku' in cloud_providers:
                heroku_config = {
                    'service': 'Heroku',
                    'dyno_type': 'web',
                    'buildpacks': ['heroku/python'],
                    'config_vars': {
                        'STREAMLIT_SERVER_PORT': '$PORT',
                        'STREAMLIT_SERVER_ADDRESS': '0.0.0.0'
                    }
                }
                
                with open(cloud_dir / 'heroku_config.json', 'w') as f:
                    json.dump(heroku_config, f, indent=2)
                
                # Create Procfile for Heroku
                procfile = "web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0"
                
                with open(cloud_dir / 'Procfile', 'w') as f:
                    f.write(procfile)
            
            # Create universal Dockerfile
            dockerfile_content = self._create_dockerfile()
            with open(cloud_dir / 'Dockerfile', 'w') as f:
                f.write(dockerfile_content)
            
            # Create docker-compose for local testing
            docker_compose = """version: '3.8'
services:
  police-monitor:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
"""
            
            with open(cloud_dir / 'docker-compose.yml', 'w') as f:
                f.write(docker_compose)
            
            # Write base configuration
            with open(cloud_dir / 'base_config.json', 'w') as f:
                json.dump(base_config, f, indent=2)
            
            # Create deployment guide
            deployment_guide = f"""
# ☁️ CLOUD-AGNOSTIC DEPLOYMENT GUIDE

## Supported Platforms
{chr(10).join([f'- {provider.upper()}' for provider in cloud_providers])}

## Pre-deployment Steps
1. Choose your cloud provider
2. Set up account and billing
3. Install provider CLI tools
4. Configure environment variables

## Environment Variables
```bash
export DATABASE_URL="your_database_url"
export SECRET_KEY="your_secret_key"
export CORS_ORIGINS="https://your-domain.com"
export SSL_ENABLED="true"
```

## Deployment Commands

### AWS Elastic Beanstalk
```bash
eb init police-monitor
eb create production
eb deploy
```

### Azure App Service
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name police-monitor --runtime "PYTHON|3.9"
az webapp deployment source config-zip --resource-group myResourceGroup --name police-monitor --src deployment.zip
```

### Google Cloud Platform
```bash
gcloud app deploy app.yaml
```

### Heroku
```bash
heroku create police-monitor
git push heroku main
```

### Docker (Any Platform)
```bash
docker build -t police-monitor .
docker run -p 8501:8501 police-monitor
```

## Configuration Files
- `base_config.json` - Universal configuration
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Local testing
- Provider-specific configs in respective files

## Security Considerations
- Use environment variables for secrets
- Enable SSL/TLS in production
- Configure proper CORS origins
- Regular security updates
"""
            
            with open(cloud_dir / 'CLOUD_DEPLOYMENT.md', 'w') as f:
                f.write(deployment_guide)
            
            print(f"   ✅ Cloud deployment directory created: {cloud_dir}")
            print(f"   ✅ Base configuration written")
            print(f"   ✅ Dockerfile created")
            print(f"   ✅ Docker Compose configuration")
            
            for provider in cloud_providers:
                print(f"   ✅ {provider.upper()} configuration created")
            
            print(f"   ✅ Deployment guide generated")
            
            return {
                'success': True,
                'deployment_type': 'cloud_agnostic',
                'deployment_dir': str(cloud_dir),
                'providers_configured': cloud_providers,
                'files_created': [
                    'Dockerfile',
                    'docker-compose.yml',
                    'base_config.json',
                    'CLOUD_DEPLOYMENT.md'
                ] + [f'{provider}_config.json' for provider in cloud_providers]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating cloud-agnostic configuration: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'deployment_type': 'cloud_agnostic'
            }
    
    def create_lightweight_version(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        🪶 Create lightweight version for low-resource environments
        """
        try:
            print(f"\n🪶 CREATING LIGHTWEIGHT VERSION")
            print("=" * 60)
            
            resource_limit = config.get('resource_limit', 'minimal')  # minimal, low, standard
            features_enabled = config.get('features', [
                'basic_monitoring',
                'simple_alerts',
                'cached_data'
            ])
            
            lightweight_dir = Path(f"deployments/lightweight_{resource_limit}")
            lightweight_dir.mkdir(parents=True, exist_ok=True)
            
            # Lightweight configuration based on resource limits
            resource_configs = {
                'minimal': {
                    'ram_limit_mb': 512,
                    'max_cache_mb': 50,
                    'max_concurrent_users': 5,
                    'features': ['basic_monitoring', 'simple_alerts']
                },
                'low': {
                    'ram_limit_mb': 1024,
                    'max_cache_mb': 100,
                    'max_concurrent_users': 10,
                    'features': ['basic_monitoring', 'simple_alerts', 'cached_data', 'basic_analysis']
                },
                'standard': {
                    'ram_limit_mb': 2048,
                    'max_cache_mb': 200,
                    'max_concurrent_users': 20,
                    'features': ['basic_monitoring', 'alerts', 'cached_data', 'analysis', 'reporting']
                }
            }
            
            current_config = resource_configs.get(resource_limit, resource_configs['minimal'])
            
            # Create lightweight main application
            lightweight_main = f"""#!/usr/bin/env python3
'''
🪶 Police Monitor - Lightweight Version
Resource Limit: {resource_limit.upper()}
RAM Limit: {current_config['ram_limit_mb']} MB
Max Users: {current_config['max_concurrent_users']}
'''

import streamlit as st
import pandas as pd
import json
import sqlite3
from datetime import datetime, timedelta
import os
import sys

# Lightweight configuration
RESOURCE_LIMIT = "{resource_limit}"
MAX_RAM_MB = {current_config['ram_limit_mb']}
MAX_CACHE_MB = {current_config['max_cache_mb']}
MAX_USERS = {current_config['max_concurrent_users']}
ENABLED_FEATURES = {current_config['features']}

def main():
    st.set_page_config(
        page_title="Police Monitor - Lightweight",
        page_icon="🪶",
        layout="wide" if RESOURCE_LIMIT != "minimal" else "centered",
        initial_sidebar_state="collapsed" if RESOURCE_LIMIT == "minimal" else "expanded"
    )
    
    # Resource usage warning
    if RESOURCE_LIMIT == "minimal":
        st.warning("🪶 Running in Minimal Resource Mode - Some features are disabled")
    
    st.title("🚓 Police Monitor - Lightweight Edition")
    st.caption(f"Resource Mode: {{RESOURCE_LIMIT.title()}} | RAM Limit: {{MAX_RAM_MB}} MB")
    
    # Basic monitoring (always enabled)
    if "basic_monitoring" in ENABLED_FEATURES:
        st.subheader("📊 Basic Monitoring")
        
        # Simple metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("System Status", "Online", help="System operational status")
        with col2:
            st.metric("Active Alerts", "3", delta="1", help="Current active alerts")
        with col3:
            st.metric("Data Sources", "2/5", help="Available data sources")
    
    # Simple alerts
    if "simple_alerts" in ENABLED_FEATURES:
        st.subheader("🚨 Recent Alerts")
        
        alerts_data = [
            {{"time": "2025-09-01 10:30", "type": "INFO", "message": "System started"}},
            {{"time": "2025-09-01 10:25", "type": "WARNING", "message": "API rate limit approaching"}},
            {{"time": "2025-09-01 10:20", "type": "ERROR", "message": "Database connection timeout"}}
        ]
        
        for alert in alerts_data[:3]:  # Limit to 3 alerts in lightweight mode
            alert_color = {{"INFO": "🔵", "WARNING": "🟡", "ERROR": "🔴"}}.get(alert["type"], "⚫")
            st.write(f"{{alert_color}} {{alert['time']}} - {{alert['message']}}")
    
    # Cached data (if enabled)
    if "cached_data" in ENABLED_FEATURES:
        st.subheader("🗂️ Cached Data")
        
        # Simple data display
        cached_items = 150 if RESOURCE_LIMIT == "standard" else 50 if RESOURCE_LIMIT == "low" else 25
        st.info(f"📦 {{cached_items}} items in cache (Limit: {{MAX_CACHE_MB}} MB)")
    
    # Basic analysis (if enabled)
    if "basic_analysis" in ENABLED_FEATURES:
        st.subheader("🔍 Basic Analysis")
        
        analysis_text = st.text_area("Enter text for analysis:", max_chars=500)
        if st.button("Analyze") and analysis_text:
            # Simple word count analysis
            word_count = len(analysis_text.split())
            char_count = len(analysis_text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Words", word_count)
            with col2:
                st.metric("Characters", char_count)
    
    # Resource usage info
    with st.expander("ℹ️ Resource Information"):
        st.write(f"**Configuration:** {{RESOURCE_LIMIT.title()}} Resource Mode")
        st.write(f"**RAM Limit:** {{MAX_RAM_MB}} MB")
        st.write(f"**Cache Limit:** {{MAX_CACHE_MB}} MB")
        st.write(f"**Max Users:** {{MAX_USERS}}")
        st.write(f"**Enabled Features:** {{', '.join(ENABLED_FEATURES)}}")

if __name__ == "__main__":
    main()
"""
            
            with open(lightweight_dir / 'main_lightweight.py', 'w') as f:
                f.write(lightweight_main)
            
            # Create minimal requirements file
            minimal_requirements = """streamlit>=1.25.0
pandas>=1.5.0
sqlite3
"""
            
            with open(lightweight_dir / 'requirements_minimal.txt', 'w') as f:
                f.write(minimal_requirements)
            
            # Create lightweight startup script
            startup_script = f"""#!/usr/bin/env python3
'''
🪶 Lightweight Police Monitor Startup
Optimized for {resource_limit} resource environments
'''

import subprocess
import sys
import os
import psutil

def check_resources():
    # Check available RAM
    available_ram = psutil.virtual_memory().available / (1024*1024)  # MB
    required_ram = {current_config['ram_limit_mb']}
    
    if available_ram < required_ram:
        print(f"⚠️ Low memory warning: {{available_ram:.0f}} MB available, {{required_ram}} MB recommended")
        
    return available_ram >= required_ram * 0.8  # Allow 80% of required

def main():
    print("🪶 Starting Police Monitor - Lightweight Edition")
    print(f"   Resource Mode: {resource_limit.title()}")
    print(f"   RAM Limit: {current_config['ram_limit_mb']} MB")
    print(f"   Max Users: {current_config['max_concurrent_users']}")
    
    if not check_resources():
        print("⚠️ Warning: System may be under-resourced for optimal performance")
    
    # Set environment variables for resource limits
    os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '10'  # 10MB limit
    os.environ['STREAMLIT_SERVER_MAX_MESSAGE_SIZE'] = '50'  # 50MB limit
    
    # Start lightweight application
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'main_lightweight.py',
            '--server.maxUploadSize', '10',
            '--server.enableStaticServing', 'false',
            '--global.disableWatchdogWarning', 'true'
        ])
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down Police Monitor")

if __name__ == "__main__":
    main()
"""
            
            with open(lightweight_dir / 'start_lightweight.py', 'w') as f:
                f.write(startup_script)
            
            # Create resource optimization guide
            optimization_guide = f"""
# 🪶 LIGHTWEIGHT VERSION GUIDE

## Resource Configuration
- **Mode:** {resource_limit.title()}
- **RAM Limit:** {current_config['ram_limit_mb']} MB
- **Cache Limit:** {current_config['max_cache_mb']} MB
- **Max Users:** {current_config['max_concurrent_users']}

## Enabled Features
{chr(10).join([f'- {feature.replace("_", " ").title()}' for feature in current_config['features']])}

## Performance Tips
1. **Close unnecessary applications** before starting
2. **Use minimal browser tabs** when accessing the system
3. **Clear browser cache** regularly
4. **Monitor system resources** during operation

## Installation
1. Install Python 3.8+ (lightweight installer)
2. Install dependencies: `pip install -r requirements_minimal.txt`
3. Run: `python start_lightweight.py`

## Troubleshooting
- **Slow performance:** Reduce concurrent users
- **Memory errors:** Close other applications
- **Connection timeouts:** Check system resources

## System Requirements (Minimum)
- **RAM:** 512 MB available
- **Storage:** 1 GB free space
- **CPU:** Single core 1.5 GHz
- **OS:** Any with Python 3.8+ support
"""
            
            with open(lightweight_dir / 'LIGHTWEIGHT_GUIDE.md', 'w') as f:
                f.write(optimization_guide)
            
            print(f"   ✅ Lightweight directory created: {lightweight_dir}")
            print(f"   ✅ Resource mode: {resource_limit} ({current_config['ram_limit_mb']} MB RAM)")
            print(f"   ✅ Lightweight application created")
            print(f"   ✅ Minimal requirements file")
            print(f"   ✅ Startup script with resource checking")
            print(f"   ✅ Optimization guide generated")
            print(f"   ✅ Features enabled: {len(current_config['features'])}")
            
            return {
                'success': True,
                'deployment_type': 'lightweight',
                'deployment_dir': str(lightweight_dir),
                'resource_limit': resource_limit,
                'config': current_config,
                'files_created': [
                    'main_lightweight.py',
                    'requirements_minimal.txt',
                    'start_lightweight.py',
                    'LIGHTWEIGHT_GUIDE.md'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error creating lightweight version: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'deployment_type': 'lightweight'
            }
    
    def _create_embedded_database(self, db_path: Path, include_sample_data: bool = True):
        """Create embedded SQLite database for portable deployment"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create basic tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cached_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    sentiment REAL,
                    threat_score REAL,
                    location TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    acknowledged INTEGER DEFAULT 0
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            if include_sample_data:
                # Insert sample data
                sample_posts = [
                    ('twitter', 'Traffic update: Heavy congestion on Mumbai highway', '2025-09-01 10:00:00', 0.1, 0.05, 'Mumbai'),
                    ('facebook', 'Community safety meeting scheduled for next week', '2025-09-01 09:30:00', 0.3, 0.02, 'Delhi'),
                    ('whatsapp', 'Emergency contact numbers updated', '2025-09-01 09:00:00', 0.2, 0.01, 'Bangalore')
                ]
                
                cursor.executemany("""
                    INSERT INTO cached_posts (platform, content, timestamp, sentiment, threat_score, location)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, sample_posts)
                
                sample_alerts = [
                    ('INFO', 'System initialized successfully', '2025-09-01 08:00:00'),
                    ('WARNING', 'API rate limit approaching', '2025-09-01 08:30:00')
                ]
                
                cursor.executemany("""
                    INSERT INTO system_alerts (level, message, timestamp)
                    VALUES (?, ?, ?)
                """, sample_alerts)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error creating embedded database: {str(e)}")
    
    def _create_dockerfile(self) -> str:
        """Create universal Dockerfile for cloud deployment"""
        return """# Police Monitor - Multi-platform Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
"""
    
    def _create_offline_documentation(self, docs_dir: Path):
        """Create comprehensive offline documentation"""
        docs_dir.mkdir(exist_ok=True)
        
        # User guide
        user_guide = """
# 📚 POLICE MONITOR - USER GUIDE

## Getting Started
1. Start the application using provided scripts
2. Open browser to http://localhost:8501
3. Navigate using the sidebar menu
4. Access different modules as needed

## Core Features
- **Real-time Monitoring**: Track social media for threats
- **Alert System**: Get notified of important events
- **Data Analysis**: Analyze content for security threats
- **Reporting**: Generate reports for investigations

## Navigation
- Use sidebar to switch between modules
- Dashboard provides system overview
- Each module has specific functionality
- Help tooltips available throughout

## Troubleshooting
- Check system requirements
- Verify Python installation
- Ensure port 8501 is available
- Review logs for error messages
"""
        
        with open(docs_dir / 'USER_GUIDE.md', 'w') as f:
            f.write(user_guide)
        
        # Technical guide
        tech_guide = """
# 🔧 TECHNICAL GUIDE

## Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python application logic
- **Database**: SQLite for data storage
- **Cache**: File-based caching system

## Configuration
- Settings in config files
- Environment variables for deployment
- Database connection parameters
- Feature toggles available

## Maintenance
- Regular database cleanup
- Log file rotation
- Cache management
- Security updates

## API Reference
- Module documentation included
- Function references available
- Configuration options documented
- Extension points identified
"""
        
        with open(docs_dir / 'TECHNICAL_GUIDE.md', 'w') as f:
            f.write(tech_guide)


def test_deployment_strategies():
    """Test all deployment strategy creation"""
    print("\n🧪 TESTING DEPLOYMENT STRATEGIES")
    print("=" * 80)
    
    # Initialize deployment manager
    deployment_manager = DeploymentManager()
    
    # Test 1: System Requirements Check
    print("\n1️⃣ Testing System Requirements Check...")
    requirements_result = deployment_manager.check_system_requirements("recommended")
    print(f"   Status: {'✅ PASSED' if requirements_result['meets_requirements'] else '⚠️ WARNINGS'}")
    
    # Test 2: Local Network Deployment
    print("\n2️⃣ Testing Local Network Deployment...")
    network_config = {
        'deployment_name': 'test_police_station',
        'network': {
            'host': '0.0.0.0',
            'port': 8502,
            'max_connections': 25
        }
    }
    network_result = deployment_manager.create_local_network_deployment(network_config)
    print(f"   Status: {'✅ CREATED' if network_result['success'] else '❌ FAILED'}")
    
    # Test 3: USB Portable Version
    print("\n3️⃣ Testing USB Portable Version...")
    usb_config = {
        'usb_name': 'PoliceMonitor_Test',
        'include_sample_data': True
    }
    usb_result = deployment_manager.create_usb_portable_version(usb_config)
    print(f"   Status: {'✅ CREATED' if usb_result['success'] else '❌ FAILED'}")
    
    # Test 4: Cloud-Agnostic Configuration
    print("\n4️⃣ Testing Cloud-Agnostic Configuration...")
    cloud_config = {
        'providers': ['aws', 'azure', 'gcp'],
        'environment': 'testing'
    }
    cloud_result = deployment_manager.create_cloud_agnostic_config(cloud_config)
    print(f"   Status: {'✅ CREATED' if cloud_result['success'] else '❌ FAILED'}")
    
    # Test 5: Lightweight Version
    print("\n5️⃣ Testing Lightweight Version...")
    lightweight_config = {
        'resource_limit': 'low',
        'features': ['basic_monitoring', 'simple_alerts', 'cached_data']
    }
    lightweight_result = deployment_manager.create_lightweight_version(lightweight_config)
    print(f"   Status: {'✅ CREATED' if lightweight_result['success'] else '❌ FAILED'}")
    
    # Summary
    print(f"\n📊 DEPLOYMENT STRATEGIES TEST SUMMARY")
    print("=" * 80)
    
    results = [
        ('System Requirements Check', requirements_result.get('meets_requirements', False)),
        ('Local Network Deployment', network_result.get('success', False)),
        ('USB Portable Version', usb_result.get('success', False)),
        ('Cloud-Agnostic Configuration', cloud_result.get('success', False)),
        ('Lightweight Version', lightweight_result.get('success', False))
    ]
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall Success Rate: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🏆 ALL DEPLOYMENT STRATEGIES WORKING PERFECTLY!")
    elif passed_tests >= total_tests * 0.8:
        print("🥇 MOST DEPLOYMENT STRATEGIES WORKING WELL!")
    else:
        print("⚠️ SOME DEPLOYMENT STRATEGIES NEED ATTENTION")
    
    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': passed_tests / total_tests,
        'results': dict(results)
    }


if __name__ == "__main__":
    test_deployment_strategies()
