#!/usr/bin/env python3
"""
AFH Property Scout - Main Application
Automated search and analysis system for Adult Family Home properties
"""

import argparse
import sys
import os
from pathlib import Path
from loguru import logger
import yaml
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent))

from scrapers.property_scraper import PropertyScraper
from analyzers.afh_analyzer import AFHAnalyzer
from notifications.notification_manager import NotificationManager
from storage.database import DatabaseManager
from scheduler.daily_scheduler import DailyScheduler
from filters.property_filter import PropertyFilter

class AFHPropertyScout:
    """Main application class for AFH Property Scout"""
    
    def __init__(self, config_path="config/settings.yaml"):
        """Initialize the AFH Property Scout application"""
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_logging()
        self._load_environment()
        
        # Initialize components
        self.db_manager = DatabaseManager(self.config['database'])
        self.property_filter = PropertyFilter(self.config['property_criteria'])
        self.afh_analyzer = AFHAnalyzer(self.config['afh_analysis'])
        self.notification_manager = NotificationManager(self.config['notifications'])
        self.property_scraper = PropertyScraper(self.config['search_sources'])
        self.scheduler = DailyScheduler(self.config['schedule'])
        
        logger.info("AFH Property Scout initialized successfully")
    
    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        log_file = log_config.get('file', 'logs/afh_scout.log')
        
        # Create logs directory if it doesn't exist
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Configure loguru
        logger.remove()  # Remove default handler
        logger.add(
            sys.stdout,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        logger.add(
            log_file,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation=f"{log_config.get('max_size_mb', 10)} MB",
            retention=log_config.get('backup_count', 5)
        )
    
    def _load_environment(self):
        """Load environment variables"""
        env_file = Path(__file__).parent.parent / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            logger.info("Environment variables loaded from .env file")
        else:
            logger.warning("No .env file found. Using system environment variables only")
    
    def run_daily_search(self):
        """Run the daily property search and analysis"""
        logger.info("Starting daily AFH property search")
        
        try:
            # Search for properties from all sources
            properties = self.property_scraper.search_all_sources()
            logger.info(f"Found {len(properties)} properties from all sources")
            
            # Filter properties based on criteria
            filtered_properties = self.property_filter.filter_properties(properties)
            logger.info(f"Filtered to {len(filtered_properties)} properties matching criteria")
            
            # Analyze properties for AFH viability
            analyzed_properties = []
            for property_data in filtered_properties:
                analysis = self.afh_analyzer.analyze_property(property_data)
                if analysis['viable']:
                    analyzed_properties.append({
                        'property': property_data,
                        'analysis': analysis
                    })
            
            logger.info(f"Found {len(analyzed_properties)} viable AFH properties")
            
            # Store results in database
            self.db_manager.store_properties(analyzed_properties)
            
            # Send notifications for new viable properties
            new_properties = self.db_manager.get_new_properties()
            if new_properties:
                self.notification_manager.send_property_alerts(new_properties)
                logger.info(f"Sent notifications for {len(new_properties)} new properties")
            
            return analyzed_properties
            
        except Exception as e:
            logger.error(f"Error during daily search: {e}")
            raise
    
    def run_one_time_search(self):
        """Run a one-time property search"""
        logger.info("Starting one-time AFH property search")
        return self.run_daily_search()
    
    def check_notifications(self):
        """Check and send pending notifications"""
        logger.info("Checking for pending notifications")
        
        new_properties = self.db_manager.get_new_properties()
        if new_properties:
            self.notification_manager.send_property_alerts(new_properties)
            logger.info(f"Sent notifications for {len(new_properties)} new properties")
        else:
            logger.info("No new properties requiring notifications")
    
    def start_scheduler(self):
        """Start the daily scheduler"""
        logger.info("Starting daily scheduler")
        self.scheduler.start(self.run_daily_search)
    
    def get_property_summary(self):
        """Get a summary of all stored properties"""
        return self.db_manager.get_property_summary()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AFH Property Scout - Automated AFH Property Search")
    parser.add_argument('--daily', action='store_true', help='Run daily search')
    parser.add_argument('--search', action='store_true', help='Run one-time search')
    parser.add_argument('--notify', action='store_true', help='Check and send notifications')
    parser.add_argument('--schedule', action='store_true', help='Start daily scheduler')
    parser.add_argument('--summary', action='store_true', help='Show property summary')
    parser.add_argument('--config', default='config/settings.yaml', help='Configuration file path')
    
    args = parser.parse_args()
    
    try:
        scout = AFHPropertyScout(args.config)
        
        if args.daily:
            results = scout.run_daily_search()
            print(f"Daily search completed. Found {len(results)} viable properties.")
            
        elif args.search:
            results = scout.run_one_time_search()
            print(f"One-time search completed. Found {len(results)} viable properties.")
            
        elif args.notify:
            scout.check_notifications()
            print("Notification check completed.")
            
        elif args.schedule:
            scout.start_scheduler()
            
        elif args.summary:
            summary = scout.get_property_summary()
            print("Property Summary:")
            print(f"Total properties: {summary['total']}")
            print(f"Viable properties: {summary['viable']}")
            print(f"New properties: {summary['new']}")
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
