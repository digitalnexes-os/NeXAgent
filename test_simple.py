from simple_searcher import SimpleSearcher
from config import Config

def test_simple():
    print("🧪 Testing SimpleSearcher...")
    config = Config()
    searcher = SimpleSearcher(config)
    
    results = searcher.search_businesses("General", 10)
    print(f"Results: {len(results)}")
    for result in results[:3]:
        print(f"  - {result.get('company_name', 'No name')}")

if __name__ == "__main__":
    test_simple()