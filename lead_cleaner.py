"""
Data cleaning and validation for scraped leads - No pandas version
"""
import re
from typing import List, Dict

class LeadCleaner:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    def process_leads(self, raw_leads: List[Dict]) -> List[Dict]:
        """Clean and validate lead data"""
        cleaned_leads = []
        
        for lead in raw_leads:
            cleaned_lead = self._clean_individual_lead(lead)
            if self._validate_lead(cleaned_lead):
                cleaned_leads.append(cleaned_lead)
        
        print(f"🧹 Cleaned {len(cleaned_leads)} valid leads from {len(raw_leads)} raw results")
        return cleaned_leads
    
    def _clean_individual_lead(self, lead: Dict) -> Dict:
        """Clean individual lead record"""
        return {
            'company_name': self._clean_text(lead.get('company_name', '')),
            'website': self._validate_website(lead.get('website', '')),
            'industry': lead.get('industry', ''),
            'email': self._extract_email(lead.get('snippet', '') + ' ' + lead.get('title', '')),
            'phone': self._extract_phone(lead.get('snippet', '')),
            'source': lead.get('source', ''),
            'date_collected': lead.get('date_collected', ''),
            'title': lead.get('title', ''),
            'snippet': lead.get('snippet', '')[:200]  # Truncate long snippets
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ''
        return ' '.join(text.split()).strip()
    
    def _validate_website(self, url: str) -> str:
        """Validate and clean website URL"""
        if not url or 'google.com' in url:
            return ''
        
        # Ensure URL starts with http
        if url.startswith('http'):
            return url
        return f"https://{url}"
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text with better patterns"""
        # More comprehensive email patterns
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'Email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'contact[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
        ]
        
        for pattern in email_patterns:
            emails = re.findall(pattern, text, re.IGNORECASE)
            if emails:
                return emails[0]
        return ''
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text with better patterns"""
        # More comprehensive phone patterns
        phone_patterns = [
            r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'Phone[:\s]*(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'Tel[:\s]*(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'Call[:\s]*(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text, re.IGNORECASE)
            if phones:
                return phones[0]
        return ''
    
    def _validate_lead(self, lead: Dict) -> bool:
        """Validate if lead has minimum required data"""
        return bool(lead.get('company_name') and lead.get('website'))