"""
Test basic Google connectivity
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def test_google():
    print("🧪 Testing Google connectivity...")
    
    try:
        # Simple Chrome setup
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome opened successfully")
        
        # Try to access Google
        driver.get("https://www.google.com")
        time.sleep(3)
        
        # Check if we're on Google
        title = driver.title
        print(f"📄 Page title: {title}")
        
        if "Google" in title:
            print("🎉 Successfully accessed Google!")
            
            # Try a simple search
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys("test search")
            search_box.submit()
            time.sleep(3)
            
            print("✅ Search performed successfully!")
        else:
            print("❌ Not on Google page")
            
        driver.quit()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_google()