#!/usr/bin/env python3
"""
AFH Property Scout Setup Script
Installs dependencies and sets up the system
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'logs',
        'templates',
        'static/css',
        'static/js',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_environment():
    """Setup environment file"""
    env_file = Path('.env')
    env_example = Path('env_example.txt')
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("📝 Created .env file from template")
        print("⚠️  Please edit .env file with your actual credentials")
    elif env_file.exists():
        print("📝 .env file already exists")
    else:
        print("⚠️  No .env template found")

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        return False
    return True

def setup_database():
    """Initialize database"""
    print("🔄 Setting up database...")
    try:
        # Import and initialize database
        sys.path.append('src')
        from storage.database import DatabaseManager
        import yaml
        
        # Load config
        with open('config/settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize database
        db_manager = DatabaseManager(config['database'])
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🏠 AFH Property Scout Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Setup environment
    print("\n🔧 Setting up environment...")
    setup_environment()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Setup database
    print("\n🗄️  Setting up database...")
    if not setup_database():
        print("❌ Setup failed during database initialization")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your credentials")
    print("2. Run: python run_scout.py --search (for one-time search)")
    print("3. Run: python run_scout.py --schedule (for daily automation)")
    print("4. Run: python run_dashboard.py (for web dashboard)")
    print("\nFor help, run: python run_scout.py --help")

if __name__ == "__main__":
    main()
