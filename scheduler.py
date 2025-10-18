"""
Local automation scheduler using APScheduler
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
from datetime import datetime

class LocalScheduler:
    def __init__(self, lead_hunter):
        self.lead_hunter = lead_hunter
        self.scheduler = BackgroundScheduler()
    
    def start_daily_schedule(self):
        """Start daily automated lead hunting"""
        # Schedule daily at 9:00 AM
        self.scheduler.add_job(
            self.lead_hunter.hunt_daily_leads,
            CronTrigger(hour=9, minute=0),
            id='daily_lead_hunt'
        )
        
        # Also schedule an immediate test run
        self.scheduler.add_job(
            self.lead_hunter.hunt_daily_leads,
            'date',
            run_date=datetime.now(),
            id='initial_test_run'
        )
        
        self.scheduler.start()
        print("⏰ Scheduler started! Daily runs at 9:00 AM")
        print("🔧 Initial test run starting now...")
    
    def manual_run(self):
        """Manual trigger for immediate lead hunting"""
        print("🔄 Manual trigger started...")
        self.lead_hunter.hunt_daily_leads()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("🛑 Scheduler stopped")