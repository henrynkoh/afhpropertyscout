#!/usr/bin/env python3
"""
AFH Property Scout Runner
Main script to run the AFH property search and analysis system
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from main import AFHPropertyScout

def main():
    """Run the AFH Property Scout system"""
    
    print("🏠 AFH Property Scout - Starting System")
    print("=" * 50)
    
    try:
        # Initialize the scout system
        scout = AFHPropertyScout()
        
        print("\nSystem initialized successfully!")
        print("\nAvailable commands:")
        print("1. Run daily search: python run_scout.py --daily")
        print("2. Run one-time search: python run_scout.py --search")
        print("3. Check notifications: python run_scout.py --notify")
        print("4. Start scheduler: python run_scout.py --schedule")
        print("5. Show summary: python run_scout.py --summary")
        print("6. Run dashboard: python run_dashboard.py")
        
        # Check command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command == '--daily':
                print("\n🔄 Running daily search...")
                results = scout.run_daily_search()
                print(f"✅ Daily search completed. Found {len(results)} viable properties.")
                
            elif command == '--search':
                print("\n🔍 Running one-time search...")
                results = scout.run_one_time_search()
                print(f"✅ Search completed. Found {len(results)} viable properties.")
                
            elif command == '--notify':
                print("\n📧 Checking notifications...")
                scout.check_notifications()
                print("✅ Notification check completed.")
                
            elif command == '--schedule':
                print("\n⏰ Starting daily scheduler...")
                print("Scheduler will run daily at 8:00 AM")
                print("Press Ctrl+C to stop the scheduler")
                scout.start_scheduler()
                
            elif command == '--summary':
                print("\n📊 Property Summary:")
                summary = scout.get_property_summary()
                print(f"Total properties: {summary.get('total', 0)}")
                print(f"Viable properties: {summary.get('viable', 0)}")
                print(f"New properties: {summary.get('new', 0)}")
                print(f"Average viability score: {summary.get('average_viability_score', 0)}%")
                
            else:
                print(f"❌ Unknown command: {command}")
                print("Use --help to see available commands")
        else:
            print("\n💡 No command specified. Use --help to see available commands")
            
    except KeyboardInterrupt:
        print("\n\n👋 AFH Property Scout stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
