"""
Website Analysis Module - Scans company websites for pain points
"""
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from typing import Dict, List

class WebsiteAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def analyze_website(self, website_url: str) -> Dict:
        """Analyze company website for pain points and insights"""
        try:
            print(f"🔍 Analyzing website: {website_url}")
            
            # Initialize with default values
            analysis = {
                'website_url': website_url,
                'is_accessible': False,
                'response_time': 0,
                'has_contact_page': False,
                'has_blog': False,
                'has_modern_design': False,
                'seo_issues': [],
                'pain_points': [],
                'business_type': 'unknown',
                'content_quality': 'unknown'
            }
            
            # Check website accessibility
            start_time = time.time()
            try:
                response = self.session.get(website_url, timeout=10)
                analysis['response_time'] = round(time.time() - start_time, 2)
                
                if response.status_code == 200:
                    analysis['is_accessible'] = True
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Perform detailed analysis
                    detailed_analysis = self._analyze_content(soup, website_url)
                    analysis.update(detailed_analysis)
                    
                    # Identify pain points
                    pain_points_analysis = self._identify_pain_points(analysis)
                    analysis.update(pain_points_analysis)
                    
                else:
                    analysis['pain_points'].append(f"Website returns {response.status_code} status")
                    
            except requests.exceptions.RequestException as e:
                analysis['pain_points'].append(f"Website not accessible: {str(e)}")
            
            print(f"✅ Analysis complete: {len(analysis['pain_points'])} pain points found")
            return analysis
            
        except Exception as e:
            print(f"❌ Website analysis error: {e}")
            # Return analysis with error information
            return {
                'website_url': website_url,
                'is_accessible': False,
                'response_time': 0,
                'pain_points': [f"Analysis failed: {str(e)}"],
                'business_type': 'unknown',
                'content_quality': 'unknown',
                'has_contact_page': False,
                'has_blog': False,
                'has_modern_design': False,
                'seo_issues': []
            }
    
    def _analyze_content(self, soup: BeautifulSoup, url: str) -> Dict:
        """Analyze website content and structure"""
        analysis = {}
        
        try:
            # Check for contact page
            contact_indicators = ['contact', 'get in touch', 'reach us', 'connect']
            contact_links = []
            for indicator in contact_indicators:
                links = soup.find_all('a', string=lambda text: text and indicator in text.lower() if text else False)
                contact_links.extend(links)
            analysis['has_contact_page'] = len(contact_links) > 0
            
            # Check for blog
            blog_indicators = ['blog', 'articles', 'news', 'insights']
            blog_links = []
            for indicator in blog_indicators:
                links = soup.find_all('a', string=lambda text: text and indicator in text.lower() if text else False)
                blog_links.extend(links)
            analysis['has_blog'] = len(blog_links) > 0
            
            # Check for modern design elements
            modern_elements = ['flex', 'grid', 'bootstrap', 'react', 'vue', 'angular', 'tailwind']
            modern_design_found = False
            for element in modern_elements:
                if soup.find(attrs={'class': lambda x: x and element in str(x).lower() if x else False}):
                    modern_design_found = True
                    break
            analysis['has_modern_design'] = modern_design_found
            
            # SEO analysis
            analysis['seo_issues'] = self._check_seo_issues(soup)
            
            # Determine business type
            analysis['business_type'] = self._identify_business_type(soup, url)
            
            # Content quality
            analysis['content_quality'] = self._assess_content_quality(soup)
            
        except Exception as e:
            print(f"⚠️ Content analysis error: {e}")
            # Set default values in case of error
            analysis.update({
                'has_contact_page': False,
                'has_blog': False,
                'has_modern_design': False,
                'seo_issues': [],
                'business_type': 'unknown',
                'content_quality': 'unknown'
            })
        
        return analysis
    
    def _check_seo_issues(self, soup: BeautifulSoup) -> List[str]:
        """Check for common SEO issues"""
        issues = []
        
        try:
            # Check title tag
            title = soup.find('title')
            if not title or not title.string or len(title.string.strip()) < 10:
                issues.append("Missing or short title tag")
            
            # Check meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc or not meta_desc.get('content') or len(meta_desc['content']) < 50:
                issues.append("Missing or short meta description")
            
            # Check heading structure
            h1_count = len(soup.find_all('h1'))
            if h1_count == 0:
                issues.append("No H1 heading found")
            elif h1_count > 1:
                issues.append("Multiple H1 headings found")
            
            # Check image alt tags
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            if images_without_alt:
                issues.append(f"{len(images_without_alt)} images missing alt tags")
                
        except Exception as e:
            issues.append(f"SEO analysis error: {str(e)}")
        
        return issues
    
    def _identify_business_type(self, soup: BeautifulSoup, url: str) -> str:
        """Identify the type of business from website content"""
        try:
            text_content = soup.get_text().lower()
            
            # Business type indicators
            business_indicators = {
                'IT Startups': ['software', 'app', 'development', 'tech', 'digital', 'cloud', 'saas', 'api'],
                'E-commerce': ['shop', 'store', 'buy', 'cart', 'checkout', 'products', 'pricing', 'order'],
                'Service Business': ['services', 'consulting', 'solutions', 'agency', 'professional', 'expert'],
                'Medical': ['medical', 'health', 'clinic', 'doctor', 'hospital', 'care', 'wellness', 'therapy'],
                'Education': ['education', 'learning', 'course', 'training', 'school', 'university', 'learn'],
                'Real Estate': ['real estate', 'property', 'home', 'house', 'rent', 'buy', 'agent', 'listing']
            }
            
            for business_type, indicators in business_indicators.items():
                if any(indicator in text_content for indicator in indicators):
                    return business_type
            
            return 'General Business'
            
        except Exception as e:
            return 'Unknown'
    
    def _assess_content_quality(self, soup: BeautifulSoup) -> str:
        """Assess the quality of website content"""
        try:
            text_content = soup.get_text()
            word_count = len(text_content.split())
            
            if word_count < 100:
                return 'Poor'
            elif word_count < 500:
                return 'Basic'
            elif word_count < 2000:
                return 'Good'
            else:
                return 'Excellent'
        except:
            return 'Unknown'
    
    def _identify_pain_points(self, analysis: Dict) -> Dict:
        """Identify business pain points based on analysis"""
        pain_points = []
        
        try:
            if not analysis['is_accessible']:
                pain_points.append("Website not accessible or very slow")
            
            if not analysis.get('has_contact_page', False):
                pain_points.append("No clear contact information")
            
            if not analysis.get('has_blog', False):
                pain_points.append("No blog/content marketing")
            
            seo_issues = analysis.get('seo_issues', [])
            if seo_issues:
                pain_points.append(f"SEO issues: {', '.join(seo_issues[:2])}")
            
            if analysis.get('response_time', 0) > 3:
                pain_points.append("Slow website loading speed")
            
            if not analysis.get('has_modern_design', False):
                pain_points.append("Outdated website design")
            
            if analysis.get('content_quality', 'Unknown') in ['Poor', 'Basic']:
                pain_points.append("Limited website content")
                
        except Exception as e:
            pain_points.append(f"Pain point analysis error: {str(e)}")
        
        return {'pain_points': pain_points}