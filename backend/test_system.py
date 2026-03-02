"""
System Testing Script
Tests all components of the recommendation system
"""
import json
import os
from embeddings import EmbeddingManager
from recommender import RecommendationEngine


def test_data_exists():
    """Test if scraped data exists"""
    print("\n1. Testing Data Availability...")
    
    if not os.path.exists('data/shl_catalog.json'):
        print("✗ FAIL: data/shl_catalog.json not found")
        print("  Run: python scraper.py")
        return False
    
    with open('data/shl_catalog.json', 'r') as f:
        data = json.load(f)
    
    count = len(data)
    print(f"✓ PASS: Found {count} assessments")
    
    if count < 377:
        print(f"⚠️  WARNING: Expected 377+ assessments, got {count}")
        print("  Consider improving scraper or using Selenium")
    
    # Check data structure
    if data:
        sample = data[0]
        required_fields = ['assessment_name', 'url', 'test_type', 'description']
        missing = [f for f in required_fields if f not in sample]
        
        if missing:
            print(f"✗ FAIL: Missing fields: {missing}")
            return False
        
        print(f"✓ PASS: Data structure valid")
    
    return True


def test_embeddings():
    """Test embedding model and vector store"""
    print("\n2. Testing Embeddings & Vector Store...")
    
    try:
        em = EmbeddingManager()
        print("✓ PASS: Embedding model loaded")
    except Exception as e:
        print(f"✗ FAIL: Could not load embedding model: {e}")
        return False
    
    # Test if collection exists
    try:
        em.load_collection()
        count = em.collection.count()
        print(f"✓ PASS: Vector store loaded with {count} embeddings")
    except Exception as e:
        print(f"✗ FAIL: Could not load collection: {e}")
        print("  Run: python embeddings.py")
        return False
    
    # Test search
    try:
        results = em.search("software developer", k=5)
        print(f"✓ PASS: Search returned {len(results)} results")
    except Exception as e:
        print(f"✗ FAIL: Search failed: {e}")
        return False
    
    return True


def test_recommender():
    """Test recommendation engine"""
    print("\n3. Testing Recommendation Engine...")
    
    try:
        em = EmbeddingManager()
        em.load_collection()
        engine = RecommendationEngine(em)
        print("✓ PASS: Recommendation engine initialized")
    except Exception as e:
        print(f"✗ FAIL: Could not initialize engine: {e}")
        return False
    
    # Test query analysis
    test_queries = [
        "Java developer",
        "Leadership and communication skills",
        "Software engineer with teamwork"
    ]
    
    for query in test_queries:
        weights = engine.analyze_query(query)
        print(f"  Query: '{query}'")
        print(f"    Weights: K={weights['K']:.1f}, P={weights['P']:.1f}")
    
    print("✓ PASS: Query analysis working")
    
    # Test recommendation
    try:
        results = engine.recommend("Java developer with collaboration", top_k=10)
        k_count = sum(1 for r in results if r['test_type'] == 'K')
        p_count = len(results) - k_count
        
        print(f"✓ PASS: Generated {len(results)} recommendations")
        print(f"  Balance: {k_count} K-type, {p_count} P-type")
        
        if len(results) > 0:
            print(f"  Top result: {results[0]['assessment_name']}")
    except Exception as e:
        print(f"✗ FAIL: Recommendation failed: {e}")
        return False
    
    return True


def test_api():
    """Test API endpoints"""
    print("\n4. Testing API...")
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✓ PASS: Health endpoint working")
        else:
            print("✗ FAIL: Health endpoint returned", response.status_code)
            return False
        
        # Test recommend endpoint
        response = requests.post(
            'http://localhost:8000/recommend',
            json={'query': 'Java developer', 'top_k': 5},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ PASS: Recommend endpoint working")
            print(f"  Returned {len(data['recommendations'])} recommendations")
        else:
            print(f"✗ FAIL: Recommend endpoint returned {response.status_code}")
            return False
        
    except requests.exceptions.ConnectionError:
        print("⚠️  SKIP: API not running")
        print("  Start with: uvicorn main:app --reload")
        return None
    except Exception as e:
        print(f"✗ FAIL: API test failed: {e}")
        return False
    
    return True


def test_evaluation():
    """Test evaluation framework"""
    print("\n5. Testing Evaluation Framework...")
    
    if not os.path.exists('data/labeled_queries.json'):
        print("⚠️  SKIP: No labeled data found")
        print("  Add labeled queries to data/labeled_queries.json")
        return None
    
    try:
        with open('data/labeled_queries.json', 'r') as f:
            data = json.load(f)
        
        train_count = len(data.get('train_queries', []))
        test_count = len(data.get('test_queries', []))
        
        print(f"✓ PASS: Labeled data loaded")
        print(f"  Train queries: {train_count}")
        print(f"  Test queries: {test_count}")
        
        if test_count == 0:
            print("⚠️  WARNING: No test queries found")
        
    except Exception as e:
        print(f"✗ FAIL: Could not load labeled data: {e}")
        return False
    
    return True


def main():
    print("="*60)
    print("SHL ASSESSMENT RECOMMENDER - SYSTEM TEST")
    print("="*60)
    
    results = {
        'Data': test_data_exists(),
        'Embeddings': test_embeddings(),
        'Recommender': test_recommender(),
        'API': test_api(),
        'Evaluation': test_evaluation()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for component, result in results.items():
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:
            status = "⚠️  SKIP"
        
        print(f"{component:15} {status}")
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Fix issues before deployment.")
        return 1
    else:
        print("\n✓ All tests passed! System ready.")
        return 0


if __name__ == "__main__":
    exit(main())
