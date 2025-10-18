"""
Simple web searcher using requests and BeautifulSoup
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
import urllib.parse

class SimpleSearcher:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })
    
    def search_businesses(self, niche: str, max_results: int = 20) -> List[Dict]:
        """Search for businesses using HTTP requests"""
        search_query = self.config.get_search_query(niche)
        results = []
        
        try:
            print(f"🔍 Searching for: {search_query}")
            
            # Try multiple search engines - Bing first
            search_methods = [
                ('Bing', self._search_bing),
                ('Google', self._search_google_direct),
                ('DuckDuckGo', self._search_duckduckgo)
            ]
            
            for engine_name, method in search_methods:
                try:
                    print(f"  Trying {engine_name}...")
                    method_results = method(search_query, niche)
                    if method_results:
                        results.extend(method_results)
                        print(f"  ✅ {engine_name} succeeded with {len(method_results)} results")
                        break
                    else:
                        print(f"  ⚠️ {engine_name} returned no results")
                except Exception as e:
                    print(f"  ❌ {engine_name} failed: {e}")
                
                # Add delay between search engines
                time.sleep(random.uniform(1, 2))
            
            return results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def _search_bing(self, query: str, niche: str) -> List[Dict]:
        """Bing search - usually most reliable"""
        results = []
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.bing.com/search?q={encoded_query}&count=10"
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            result_elements = soup.select('li.b_algo')
            
            for result in result_elements[:10]:
                try:
                    title_elem = result.select_one('h2 a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href', '')
                    
                    # Skip Bing's own pages
                    if 'bing.com' in href:
                        continue
                    
                    snippet_elem = result.select_one('.b_caption p')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # Skip articles about finding contacts
                    if any(word in title.lower() for word in ['how to find', 'contact database', 'email finder', 'business lookup', 'ways to find']):
                        continue
                    
                    results.append({
                        'company_name': self._extract_company_name(title),
                        'title': title,
                        'website': href,
                        'snippet': snippet,
                        'industry': niche,
                        'source': 'Bing',
                        'date_collected': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                except:
                    continue
            
            return results
            
        except Exception as e:
            raise Exception(f"Bing search failed: {e}")
    
    def _search_google_direct(self, query: str, niche: str) -> List[Dict]:
        """Google search - may be blocked"""
        results = []
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&num=10"
        
        try:
            response = self.session.get(url, timeout=10)
            
            # Check if we got blocked
            if "detected unusual traffic" in response.text.lower():
                raise Exception("Google blocked the request")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            result_elements = soup.select('div.g')
            
            for result in result_elements[:10]:
                try:
                    title_elem = result.select_one('h3')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    link_elem = result.select_one('a')
                    href = link_elem.get('href', '') if link_elem else ""
                    
                    if href.startswith('/url?q='):
                        href = href.split('/url?q=')[1].split('&')[0]
                        href = urllib.parse.unquote(href)
                    
                    snippet_elem = result.select_one('.VwiC3b')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # Skip Google's own pages and articles
                    if not href or 'google.com' in href:
                        continue
                    
                    if any(word in title.lower() for word in ['how to find', 'contact database', 'email finder']):
                        continue
                    
                    results.append({
                        'company_name': self._extract_company_name(title),
                        'title': title,
                        'website': href,
                        'snippet': snippet,
                        'industry': niche,
                        'source': 'Google',
                        'date_collected': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                except:
                    continue
            
            return results
            
        except Exception as e:
            raise Exception(f"Google search failed: {e}")
    
    def _search_duckduckgo(self, query: str, niche: str) -> List[Dict]:
        """DuckDuckGo search with proper URL handling"""
        results = []
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            result_elements = soup.select('.result')
            
            for result in result_elements[:10]:
                try:
                    title_elem = result.select_one('.result__a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href', '')
                    
                    # Skip DuckDuckGo redirect URLs
                    if 'duckduckgo.com/l/' in href:
                        continue
                    
                    # Skip articles about finding contacts
                    if any(word in title.lower() for word in ['how to find', 'contact database', 'email finder', 'business lookup', 'ways to find']):
                        continue
                    
                    snippet_elem = result.select_one('.result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append({
                        'company_name': self._extract_company_name(title),
                        'title': title,
                        'website': href,
                        'snippet': snippet,
                        'industry': niche,
                        'source': 'DuckDuckGo',
                        'date_collected': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                except:
                    continue
            
            return results
            
        except Exception as e:
            raise Exception(f"DuckDuckGo search failed: {e}")
    
    def _extract_company_name(self, title: str) -> str:
        """Extract company name from title"""
        remove_phrases = [' - Home', ' | Official Website', ' - Contact Us', 'Official Site']
        company_name = title
        
        for phrase in remove_phrases:
            company_name = company_name.replace(phrase, '')
        
        return company_name.strip()