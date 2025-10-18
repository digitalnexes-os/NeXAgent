"""
Local configuration manager for NeXAgent
"""
import os
from datetime import datetime

class Config:
    def __init__(self):
        # Local file paths
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.OUTPUTS_DIR = os.path.join(self.BASE_DIR, 'outputs')
        self.LEADS_DIR = os.path.join(self.OUTPUTS_DIR, 'leads')
        self.REPORTS_DIR = os.path.join(self.OUTPUTS_DIR, 'reports')
        self.LOGS_DIR = os.path.join(self.BASE_DIR, 'logs')
        self.DRIVERS_DIR = os.path.join(self.BASE_DIR, 'drivers')
        
        # Create directories
        self._create_directories()
        
        # Scraping settings
        self.HEADLESS = False  # Set to True after testing
        self.TIMEOUT = 30
        self.MAX_LEADS_PER_DAY = 100
        self.DELAY_BETWEEN_REQUESTS = 2  # seconds
        
        # Niche schedule
        self.NICHE_SCHEDULE = {
            0: 'IT Startups',    # Monday
            1: 'Medical',        # Tuesday
            2: 'Education',      # Wednesday
            3: 'Real Estate',    # Thursday
            4: 'E-commerce',     # Friday
            5: 'General',        # Saturday
            6: 'General'         # Sunday
        }
        
        # Search templates for each niche
        self.SEARCH_TEMPLATES = {
    'IT Startups': 'technology',
    'Medical': 'healthcare', 
    'Education': 'education',
    'Real Estate': 'real estate',
    'E-commerce': 'retail',
    'General': 'business'
}
    
    def _create_directories(self):
        """Create all necessary directories"""
        directories = [
            self.OUTPUTS_DIR,
            self.LEADS_DIR, 
            self.REPORTS_DIR,
            self.LOGS_DIR,
            self.DRIVERS_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_todays_niche(self):
        """Get today's niche based on schedule"""
        weekday = datetime.now().weekday()
        return self.NICHE_SCHEDULE.get(weekday, 'General')
    
    def get_search_query(self, niche):
        """Get search query for niche"""
        return self.SEARCH_TEMPLATES.get(niche, niche + ' business contact email')