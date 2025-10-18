"""
CSV file management for local lead storage - Single master file version
"""
import csv
import os
from datetime import datetime
import logging

class CSVManager:
    def __init__(self, config):
        self.config = config
        self.setup_logging()
        self.master_file = os.path.join(self.config.LEADS_DIR, 'neXagent_master_leads.csv')
    
    def setup_logging(self):
        """Setup logging for CSV operations"""
        logging.basicConfig(
            filename=os.path.join(self.config.LOGS_DIR, 'neXagent.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def save_leads(self, leads: list, niche: str) -> str:
        """Save leads to master CSV file - appends to single file"""
        try:
            if not leads:
                print("⚠️ No leads to save")
                return self.master_file
            
            # Define CSV headers (removed date_collected)
            headers = [
                'timestamp', 'niche', 'company_name', 
                'website', 'industry', 'email', 'phone', 'source', 
                'title', 'snippet'
            ]
            
            # Check if master file exists
            file_exists = os.path.exists(self.master_file)
            
            # Append to master file
            with open(self.master_file, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                # Write header only if file doesn't exist
                if not file_exists:
                    writer.writeheader()
                    print("📁 Created new master leads file")
                
                # Add timestamp to each lead
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                leads_added = 0
                for lead in leads:
                    # Prepare lead data with timestamp (no date_collected)
                    lead_data = {
                        'timestamp': current_timestamp,
                        'niche': niche,
                        'company_name': lead.get('company_name', ''),
                        'website': lead.get('website', ''),
                        'industry': lead.get('industry', ''),
                        'email': lead.get('email', ''),
                        'phone': lead.get('phone', ''),
                        'source': lead.get('source', ''),
                        'title': lead.get('title', ''),
                        'snippet': lead.get('snippet', '')
                    }
                    
                    # Check if this lead already exists to avoid duplicates
                    if not self._is_duplicate_lead(lead_data):
                        writer.writerow(lead_data)
                        leads_added += 1
            
            print(f"💾 Added {leads_added} new leads to master file: {self.master_file}")
            logging.info(f"Added {leads_added} {niche} leads to master file")
            
            return self.master_file
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            logging.error(f"CSV save error: {e}")
            return self.master_file
    
    def _is_duplicate_lead(self, new_lead: dict) -> bool:
        """Check if lead already exists in master file to avoid duplicates"""
        try:
            if not os.path.exists(self.master_file):
                return False
            
            with open(self.master_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for existing_lead in reader:
                    # Check if company name and website are the same
                    if (existing_lead.get('company_name', '').strip().lower() == new_lead['company_name'].strip().lower() and
                        existing_lead.get('website', '').strip().lower() == new_lead['website'].strip().lower()):
                        return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Error checking duplicates: {e}")
            return False
    
    def get_leads_count(self) -> int:
        """Get total number of leads in master file"""
        try:
            if not os.path.exists(self.master_file):
                return 0
            
            with open(self.master_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return sum(1 for _ in reader)
                
        except Exception as e:
            print(f"⚠️ Error counting leads: {e}")
            return 0