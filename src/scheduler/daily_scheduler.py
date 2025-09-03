"""
Daily Scheduler - Handles automated daily property searches
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Callable, Dict, Any
from loguru import logger
import signal
import sys

class DailyScheduler:
    """Manages daily automated property searches"""
    
    def __init__(self, schedule_config: Dict[str, Any]):
        """Initialize daily scheduler with configuration"""
        self.config = schedule_config
        self.search_time = schedule_config.get('daily_search_time', '08:00')
        self.search_frequency_hours = schedule_config.get('search_frequency_hours', 24)
        self.notification_check_minutes = schedule_config.get('notification_check_minutes', 30)
        
        self.is_running = False
        self.search_function = None
        self.notification_function = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def start(self, search_function: Callable, notification_function: Callable = None):
        """Start the daily scheduler"""
        logger.info(f"Starting daily scheduler with search time: {self.search_time}")
        
        self.search_function = search_function
        self.notification_function = notification_function
        self.is_running = True
        
        # Schedule daily search
        schedule.every().day.at(self.search_time).do(self._run_daily_search)
        
        # Schedule notification checks
        if notification_function:
            schedule.every(self.notification_check_minutes).minutes.do(self._check_notifications)
        
        # Start scheduler in separate thread
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("Daily scheduler started successfully")
        
        # Keep main thread alive
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Scheduler interrupted by user")
            self.stop()
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("Scheduler loop started")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait before retrying
    
    def _run_daily_search(self):
        """Execute daily property search"""
        try:
            logger.info("Starting scheduled daily search")
            start_time = datetime.now()
            
            # Run the search function
            if self.search_function:
                results = self.search_function()
                
                # Log search results
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                logger.info(f"Daily search completed in {duration:.1f} seconds")
                logger.info(f"Found {len(results) if results else 0} viable properties")
                
                # Record search history
                self._record_search_history(len(results) if results else 0, duration)
                
            else:
                logger.error("No search function configured")
                
        except Exception as e:
            logger.error(f"Error during scheduled search: {e}")
            self._record_search_history(0, 0, status='failed', error=str(e))
    
    def _check_notifications(self):
        """Check for pending notifications"""
        try:
            if self.notification_function:
                logger.debug("Checking for pending notifications")
                self.notification_function()
        except Exception as e:
            logger.error(f"Error checking notifications: {e}")
    
    def _record_search_history(self, properties_found: int, duration_seconds: float, 
                             status: str = 'completed', error: str = None):
        """Record search history for tracking"""
        try:
            # This would typically integrate with the database manager
            # For now, just log the information
            logger.info(f"Search history: {properties_found} properties, {duration_seconds:.1f}s, {status}")
            if error:
                logger.error(f"Search error: {error}")
                
        except Exception as e:
            logger.error(f"Error recording search history: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        logger.info("Stopping daily scheduler")
        self.is_running = False
        schedule.clear()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully")
        self.stop()
        sys.exit(0)
    
    def get_next_run_time(self) -> str:
        """Get the next scheduled run time"""
        try:
            next_run = schedule.next_run()
            if next_run:
                return next_run.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return "No scheduled runs"
        except Exception as e:
            logger.error(f"Error getting next run time: {e}")
            return "Error"
    
    def get_schedule_status(self) -> Dict[str, Any]:
        """Get current schedule status"""
        return {
            'is_running': self.is_running,
            'search_time': self.search_time,
            'search_frequency_hours': self.search_frequency_hours,
            'notification_check_minutes': self.notification_check_minutes,
            'next_run_time': self.get_next_run_time(),
            'scheduled_jobs': len(schedule.jobs)
        }
    
    def run_immediate_search(self):
        """Run an immediate search (outside of schedule)"""
        try:
            logger.info("Running immediate search")
            if self.search_function:
                results = self.search_function()
                logger.info(f"Immediate search completed. Found {len(results) if results else 0} properties")
                return results
            else:
                logger.error("No search function configured")
                return []
        except Exception as e:
            logger.error(f"Error during immediate search: {e}")
            return []
    
    def update_schedule(self, new_search_time: str = None, new_frequency_hours: int = None):
        """Update schedule configuration"""
        try:
            if new_search_time:
                self.search_time = new_search_time
                schedule.clear()
                schedule.every().day.at(self.search_time).do(self._run_daily_search)
                logger.info(f"Updated search time to {new_search_time}")
            
            if new_frequency_hours:
                self.search_frequency_hours = new_frequency_hours
                logger.info(f"Updated search frequency to {new_frequency_hours} hours")
                
        except Exception as e:
            logger.error(f"Error updating schedule: {e}")

class SearchScheduler:
    """Alternative scheduler using APScheduler for more advanced scheduling"""
    
    def __init__(self, schedule_config: Dict[str, Any]):
        """Initialize advanced scheduler"""
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        
        self.config = schedule_config
        self.scheduler = BackgroundScheduler()
        self.search_function = None
        self.notification_function = None
        
        # Parse search time
        search_time = schedule_config.get('daily_search_time', '08:00')
        hour, minute = map(int, search_time.split(':'))
        
        # Schedule daily search
        self.scheduler.add_job(
            func=self._run_daily_search,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_search',
            name='Daily AFH Property Search',
            replace_existing=True
        )
        
        # Schedule notification checks
        notification_interval = schedule_config.get('notification_check_minutes', 30)
        self.scheduler.add_job(
            func=self._check_notifications,
            trigger='interval',
            minutes=notification_interval,
            id='notification_check',
            name='Notification Check',
            replace_existing=True
        )
    
    def start(self, search_function: Callable, notification_function: Callable = None):
        """Start the advanced scheduler"""
        logger.info("Starting advanced scheduler")
        
        self.search_function = search_function
        self.notification_function = notification_function
        
        self.scheduler.start()
        logger.info("Advanced scheduler started successfully")
    
    def stop(self):
        """Stop the advanced scheduler"""
        logger.info("Stopping advanced scheduler")
        self.scheduler.shutdown()
    
    def _run_daily_search(self):
        """Execute daily property search"""
        try:
            logger.info("Starting scheduled daily search (APScheduler)")
            start_time = datetime.now()
            
            if self.search_function:
                results = self.search_function()
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                logger.info(f"Daily search completed in {duration:.1f} seconds")
                logger.info(f"Found {len(results) if results else 0} viable properties")
                
        except Exception as e:
            logger.error(f"Error during scheduled search: {e}")
    
    def _check_notifications(self):
        """Check for pending notifications"""
        try:
            if self.notification_function:
                logger.debug("Checking for pending notifications (APScheduler)")
                self.notification_function()
        except Exception as e:
            logger.error(f"Error checking notifications: {e}")
    
    def get_job_status(self) -> Dict[str, Any]:
        """Get status of scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return {
            'scheduler_running': self.scheduler.running,
            'jobs': jobs
        }
