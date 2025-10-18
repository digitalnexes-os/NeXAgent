"""
NeXAgent - Main Application Entry Point
"""
import time
import sys
import os
from config import Config
from directory_searcher import DirectorySearcher
from lead_cleaner import LeadCleaner
from csv_manager import CSVManager
from scheduler import LocalScheduler

class NeXAgent:
    def __init__(self):
        print("🚀 Initializing NeXAgent - Phase 1: AI Lead Hunter")
        
        # Initialize components
        self.config = Config()
        self.searcher = DirectorySearcher(self.config)  # Using DirectorySearcher
        self.cleaner = LeadCleaner()
        self.csv_manager = CSVManager(self.config)
        self.scheduler = LocalScheduler(self)
        
        print("✅ NeXAgent initialized successfully!")
    
    def hunt_daily_leads(self):
        """Main method to execute daily lead hunting"""
        try:
            print("\n" + "="*50)
            print(f"🎯 Starting Daily Lead Hunt - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Get today's niche
            niche = self.config.get_todays_niche()
            print(f"📊 Target Niche: {niche}")
            
            # Search for leads using DirectorySearcher
            print("🔍 Searching business directories...")
            raw_leads = self.searcher.search_businesses(niche, 20)
            
            if not raw_leads:
                print("❌ No leads found from directories.")
                return
            
            # Clean and process leads
            print("🧹 Cleaning and validating leads...")
            cleaned_leads = self.cleaner.process_leads(raw_leads)
            
            if not cleaned_leads:
                print("❌ No valid leads after cleaning.")
                return
            
            # Save to CSV
            print("💾 Saving leads to CSV...")
            saved_path = self.csv_manager.save_leads(cleaned_leads, niche)
            
            # Generate report
            self._generate_daily_report(cleaned_leads, niche, saved_path)
            
            print(f"✅ Daily hunt completed! Found {len(cleaned_leads)} valid leads.")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"❌ Error in daily lead hunt: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_daily_report(self, leads, niche, filepath):
        """Generate daily summary report"""
        total_leads_in_system = self.csv_manager.get_leads_count()
        
        report = {
            'date': time.strftime('%Y-%m-%d'),
            'niche': niche,
            'new_leads_added': len(leads),
            'leads_with_email': len([l for l in leads if l['email']]),
            'leads_with_phone': len([l for l in leads if l['phone']]),
            'total_leads_in_system': total_leads_in_system,
            'file_location': filepath,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print("\n📈 DAILY REPORT:")
        print(f"   Date: {report['date']}")
        print(f"   Niche: {report['niche']}")
        print(f"   New Leads Added: {report['new_leads_added']}")
        print(f"   Leads with Email: {report['leads_with_email']}")
        print(f"   Leads with Phone: {report['leads_with_phone']}")
        print(f"   Total Leads in System: {report['total_leads_in_system']}")
        print(f"   Master File: {report['file_location']}")

def main():
    """Main application entry point"""
    try:
        agent = NeXAgent()
        
        # Interactive mode
        print("\n🤖 How do you want to run NeXAgent?")
        print("1. Manual run (once)")
        print("2. Start scheduler (runs daily at 9 AM)")
        
        choice = input("\nEnter choice (1-2): ").strip()
        
        if choice == '1':
            agent.hunt_daily_leads()
        elif choice == '2':
            agent.scheduler.start_daily_schedule()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                agent.scheduler.stop_scheduler()
        else:
            print("❌ Invalid choice. Exiting.")
                
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()