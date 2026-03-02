"""
Export recommendations to CSV format for submission
"""
import json
import csv
from recommender import RecommendationEngine
from embeddings import EmbeddingManager


def export_test_results(test_queries_file: str = "data/labeled_queries.json",
                        output_file: str = "data/submission.csv"):
    """Export test query recommendations to CSV"""
    
    # Load engine
    em = EmbeddingManager()
    em.load_collection()
    engine = RecommendationEngine(em)
    
    # Load test queries
    with open(test_queries_file, 'r') as f:
        data = json.load(f)
    
    test_queries = data.get('test_queries', [])
    
    # Generate recommendations
    rows = []
    
    for query_data in test_queries:
        query = query_data['query']
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
    
    print(f"✓ Exported {len(rows)} rows to {output_file}")
    print(f"  {len(test_queries)} queries × 10 recommendations = {len(rows)} rows")


if __name__ == "__main__":
    export_test_results()
