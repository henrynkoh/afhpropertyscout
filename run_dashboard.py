#!/usr/bin/env python3
"""
AFH Property Scout Dashboard Runner
Starts the web dashboard for monitoring AFH property searches
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from dashboard.dashboard import AFHDashboard, create_dashboard_templates
from storage.database import DatabaseManager
import yaml

def main():
    """Run the AFH Property Scout Dashboard"""
    
    # Load configuration
    config_path = 'config/settings.yaml'
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        print("Please ensure config/settings.yaml exists")
        sys.exit(1)
    
    # Create dashboard templates
    create_dashboard_templates()
    
    # Initialize database manager
    db_manager = DatabaseManager(config['database'])
    
    # Create and run dashboard
    dashboard = AFHDashboard(db_manager, config)
    
    print("Starting AFH Property Scout Dashboard...")
    print("Dashboard will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        dashboard.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error running dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
