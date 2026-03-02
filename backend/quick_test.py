"""
Quick test script using sample data
Run this to verify the system works before scraping real data
"""
import json
import os
from embeddings import EmbeddingManager
from recommender import RecommendationEngine


def setup_sample_data():
    """Use sample data for quick testing"""
    sample_file = "data/sample_catalog.json"
    target_file = "data/shl_catalog.json"
    
    if not os.path.exists(target_file):
        print("Using sample data for testing...")
        with open(sample_file, 'r') as f:
            data = json.load(f)
        with open(target_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Created {target_file} with {len(data)} sample assessments")
        return True
    else:
        print(f"✓ Using existing {target_file}")
        return False


def build_sample_index():
    """Build index from sample data"""
    print("\nBuilding vector index...")
    
    with open("data/shl_catalog.json", 'r') as f:
        assessments = json.load(f)
    
    em = EmbeddingManager()
    em.build_index(assessments)
    
    print(f"✓ Index built with {len(assessments)} assessments")
    return em


def test_recommendations(em):
    """Test recommendation engine"""
    print("\nTesting recommendation engine...")
    
    engine = RecommendationEngine(em)
    
    test_queries = [
        "Java developer with collaboration skills",
        "Leadership role with strategic thinking",
        "Customer service with communication skills"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        results = engine.recommend(query, top_k=5)
        
        k_count = sum(1 for r in results if r['test_type'] == 'K')
        p_count = len(results) - k_count
        
        print(f"Balance: {k_count} K-type, {p_count} P-type\n")
        
        for i, rec in enumerate(results, 1):
            print(f"{i}. [{rec['test_type']}] {rec['assessment_name']}")
            print(f"   {rec['description'][:80]}...")
            print()


def main():
    print("="*60)
    print("QUICK TEST - SHL Assessment Recommender")
    print("="*60)
    print("\nThis script uses sample data to verify the system works.")
    print("For production, run the full scraper to get 377+ assessments.\n")
    
    # Setup sample data
    is_new = setup_sample_data()
    
    # Build or load index
    if is_new or not os.path.exists("chroma_db"):
        em = build_sample_index()
    else:
        print("\nLoading existing index...")
        em = EmbeddingManager()
        em.load_collection()
        print(f"✓ Loaded index with {em.collection.count()} embeddings")
    
    # Test recommendations
    test_recommendations(em)
    
    print("\n" + "="*60)
    print("QUICK TEST COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Run full scraper: python scraper.py")
    print("2. Rebuild index: python embeddings.py")
    print("3. Add labeled queries: data/labeled_queries.json")
    print("4. Run evaluation: python evaluate.py")
    print("5. Start API: uvicorn main:app --reload")


if __name__ == "__main__":
    main()
