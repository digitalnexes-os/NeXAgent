"""
Google Search scraper with human-like behavior
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
from typing import List, Dict

class GoogleSearcher:
    def __init__(self, config):
        self.config = config
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with human-like behavior"""
        try:
            chrome_options = Options()
            
            if self.config.HEADLESS:
                chrome_options.add_argument("--headless")
            
            # Human-like browser settings
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Automatic driver management
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver initialized successfully")
            
        except Exception as e:
            print(f"❌ Chrome driver error: {e}")
            print("💡 Please ensure Chrome is installed on your system")
            raise
    
    def search_businesses(self, niche: str, max_results: int = 15) -> List[Dict]:
        """Search for businesses with human-like delays"""
        search_query = self.config.get_search_query(niche)
        results = []
        
        try:
            print(f"🔍 Searching for: {search_query}")
            
            # Navigate to Google with human-like delay
            self.driver.get("https://www.google.com")
            self._human_delay(3, 5)  # Wait 3-5 seconds
            
            # Handle cookies
            self._handle_cookies()
            
            # Find search box and type slowly
            search_box = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Clear and type like a human
            search_box.clear()
            self._type_like_human(search_box, search_query)
            
            # Submit search
            search_box.submit()
            self._human_delay(4, 6)  # Wait for results
            
            # Extract results from first page
            print("📄 Extracting search results...")
            page_results = self._extract_page_results(niche)
            results.extend(page_results)
            
            print(f"✅ Found {len(results)} results for {niche}")
            return results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            import traceback
            traceback.print_exc()
            return results
        finally:
            self._safe_driver_quit()
    
    def _human_delay(self, min_seconds=2, max_seconds=4):
        """Human-like random delay"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def _type_like_human(self, element, text):
        """Type text like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Random typing speed
    
    def _handle_cookies(self):
        """Handle cookie consent popup"""
        try:
            # Wait a bit before checking for cookies
            time.sleep(2)
            
            # Try different cookie button selectors
            cookie_selectors = [
                "//button/div[contains(., 'Accept all')]",
                "//button[contains(., 'Accept all')]",
                "//button[contains(., 'I agree')]",
                "//button[@id='L2AGLb']",  # Google's accept button ID
                "//div[@role='button']//span[contains(., 'Accept')]"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    cookie_button.click()
                    print("✅ Accepted cookies")
                    time.sleep(1)
                    return
                except:
                    continue
                    
        except Exception as e:
            pass  # No cookie popup found
    
    def _extract_page_results(self, niche: str) -> List[Dict]:
        """Extract results from current page"""
        results = []
        
        try:
            # Wait for search results with multiple selector attempts
            selectors_to_try = [
                ("div.g", "CSS selector"),
                ("//div[@class='g']", "XPath"),
                ("div[class*='g ']", "CSS partial class"),
                ("div[data-sokoban-container]", "CSS data attribute")
            ]
            
            results_found = False
            for selector, selector_type in selectors_to_try:
                try:
                    if selector_type == "CSS selector":
                        WebDriverWait(self.driver, 8).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                    else:  # XPath
                        WebDriverWait(self.driver, 8).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    
                    print(f"✅ Found results using {selector_type}: {selector}")
                    results_found = True
                    break
                except TimeoutException:
                    continue
            
            if not results_found:
                print("⚠️ No standard result selectors found, trying fallback...")
                # Fallback: look for any result-like elements
                try:
                    possible_results = self.driver.find_elements(By.CSS_SELECTOR, "div")
                    possible_results = [el for el in possible_results if el.get_attribute('class') and 'g' in el.get_attribute('class')]
                    if possible_results:
                        results_found = True
                        print(f"✅ Found {len(possible_results)} possible results using fallback")
                except:
                    pass
            
            if results_found:
                # Try to extract results using multiple selectors
                result_elements = []
                
                for selector, selector_type in selectors_to_try:
                    try:
                        if selector_type == "CSS selector":
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        else:  # XPath
                            elements = self.driver.find_elements(By.XPATH, selector)
                        
                        if elements:
                            result_elements = elements
                            print(f"📊 Found {len(result_elements)} result elements")
                            break
                    except:
                        continue
                
                # Process each result
                for result in result_elements[:10]:  # Limit to first 10 results
                    try:
                        lead_data = self._extract_lead_data(result, niche)
                        if lead_data and lead_data.get('company_name'):
                            results.append(lead_data)
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Error extracting results: {e}")
        
        return results
    
    def _extract_lead_data(self, result, niche: str) -> Dict:
        """Extract data from individual search result"""
        try:
            # Get title using multiple selectors
            title = ""
            title_selectors = [
                "h3",
                "a h3", 
                "div[role='heading'] h3",
                "div[class*='title']",
                ".LC20lb"
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = result.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title:
                        break
                except:
                    continue
            
            if not title:
                return None
            
            # Get URL
            url = ""
            try:
                link_elem = result.find_element(By.CSS_SELECTOR, "a")
                url = link_elem.get_attribute("href")
                if "google.com" in url:  # Skip Google's own links
                    return None
            except:
                pass
            
            # Get snippet
            snippet = ""
            snippet_selectors = [
                "div.VwiC3b",
                "div[class*='snippet']",
                "span[class*='snippet']",
                ".VwiC3b"
            ]
            
            for selector in snippet_selectors:
                try:
                    snippet_elem = result.find_element(By.CSS_SELECTOR, selector)
                    snippet = snippet_elem.text.strip()
                    if snippet:
                        break
                except:
                    continue
            
            return {
                'company_name': self._extract_company_name(title),
                'title': title,
                'website': url,
                'snippet': snippet,
                'industry': niche,
                'source': 'Google Search',
                'date_collected': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return None
    
    def _extract_company_name(self, title: str) -> str:
        """Extract company name from title"""
        remove_phrases = [' - Home', ' | Official Website', ' - Contact Us', 'Official Site']
        company_name = title
        
        for phrase in remove_phrases:
            company_name = company_name.replace(phrase, '')
        
        return company_name.strip()
    
    def _safe_driver_quit(self):
        """Safely quit driver"""
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"⚠️ Error closing driver: {e}")