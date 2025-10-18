from website_analyzer import WebsiteAnalyzer

def test_analyzer():
    analyzer = WebsiteAnalyzer()
    
    test_websites = [
        "https://www.google.com",
        "https://www.shopify.com", 
        "https://www.hubspot.com",
        "https://www.amazon.com"
    ]
    
    for website in test_websites:
        print(f"\n{'='*50}")
        result = analyzer.analyze_website(website)
        print(f"📊 Analysis for: {website}")
        print(f"✅ Accessible: {result.get('is_accessible', False)}")
        print(f"⏱️ Response Time: {result.get('response_time', 0)}s")
        print(f"🏢 Business Type: {result.get('business_type', 'unknown')}")
        print(f"📝 Pain Points: {result.get('pain_points', [])}")
        print(f"🔧 SEO Issues: {result.get('seo_issues', [])}")

if __name__ == "__main__":
    test_analyzer()