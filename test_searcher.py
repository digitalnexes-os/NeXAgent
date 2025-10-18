"""
Test searcher with sample data to verify the system works
"""
import time
from typing import List, Dict
import random

class TestSearcher:
    def __init__(self, config):
        self.config = config
    
    def search_businesses(self, niche: str, max_results: int = 20) -> List[Dict]:
        """Generate sample business data for testing"""
        print(f"🔍 Testing with sample data for: {niche}")
        
        # Sample business data
        sample_businesses = [
            {
                'company_name': 'Tech Solutions Inc',
                'website': 'https://techsolutions.com',
                'industry': niche,
                'email': 'contact@techsolutions.com',
                'phone': '+1-555-0123',
                'source': 'Sample Data',
                'date_collected': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': 'Tech Solutions Inc - Contact Us',
                'snippet': 'Leading software development company offering custom solutions. Contact us for inquiries.'
            },
            {
                'company_name': 'Global Medical Services',
                'website': 'https://globalmedical.com',
                'industry': niche,
                'email': 'info@globalmedical.com', 
                'phone': '+1-555-0124',
                'source': 'Sample Data',
                'date_collected': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': 'Global Medical Services - Healthcare',
                'snippet': 'Providing quality healthcare services. Email us for appointments.'
            },
            {
                'company_name': 'EduLearn Academy',
                'website': 'https://edulearn.com',
                'industry': niche,
                'email': 'admissions@edulearn.com',
                'phone': '+1-555-0125',
                'source': 'Sample Data',
                'date_collected': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': 'EduLearn Academy - Admissions',
                'snippet': 'Online education platform. Contact admissions for course information.'
            },
            {
                'company_name': 'Prime Real Estate',
                'website': 'https://primerealestate.com',
                'industry': niche,
                'email': 'agents@primerealestate.com',
                'phone': '+1-555-0126',
                'source': 'Sample Data',
                'date_collected': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': 'Prime Real Estate - Find Your Dream Home',
                'snippet': 'Real estate agency helping you find perfect properties. Call our agents.'
            },
            {
                'company_name': 'ShopEasy Online',
                'website': 'https://shopeasy.com',
                'industry': niche,
                'email': 'support@shopeasy.com',
                'phone': '+1-555-0127',
                'source': 'Sample Data',
                'date_collected': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': 'ShopEasy Online - Ecommerce Store',
                'snippet': 'Your one-stop online shopping destination. Contact support for help.'
            }
        ]
        
        # Return random sample of businesses
        num_results = min(max_results, len(sample_businesses))
        results = random.sample(sample_businesses, num_results)
        
        print(f"✅ Generated {len(results)} sample leads for testing")
        return results