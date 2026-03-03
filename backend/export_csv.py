"""
Export recommendations to CSV format for submission
Format: Query, Assessment_url (one row per recommendation)
"""
import json
import csv
from recommender import RecommendationEngine
from embeddings import EmbeddingManager


def export_test_results(test_queries_file: str = "data/labeled_queries.json",
                        output_file: str = "data/submission.csv"):
    """Export test query recommendations to CSV in submission format"""
    
    # Load engine
    print("Loading recommendation engine...")
    em = EmbeddingManager()
    try:
        em.load_collection()
    except:
        print("Building new collection...")
        import os
        catalog_file = "data/shl_catalog.json" if os.path.exists("data/shl_catalog.json") else "data/sample_catalog.json"
        with open(catalog_file, 'r', encoding='utf-8') as f:
            assessments = json.load(f)
        em.build_index(assessments)
    
    engine = RecommendationEngine(em)
    
    # Load test queries
    with open(test_queries_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_queries = data.get('test_queries', [])
    
    if not test_queries:
        print("⚠️  No test queries found in file")
        return
    
    # Generate recommendations
    rows = []
    
    print(f"\nGenerating recommendations for {len(test_queries)} queries...")
    for i, query_data in enumerate(test_queries, 1):
        query = query_data['query']
        print(f"  {i}. {query[:60]}...")
        
        recommendations = engine.recommend(query, top_k=10)
        
        for rec in recommendations:
            rows.append({
                'Query': query,
                'Assessment_url': rec['url']
            })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Query', 'Assessment_url'])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✓ Exported {len(rows)} rows to {output_file}")
    print(f"  Format: {len(test_queries)} queries × up to 10 recommendations")
    print(f"\nSubmission file ready: {output_file}")


if __name__ == "__main__":
    export_test_results()
