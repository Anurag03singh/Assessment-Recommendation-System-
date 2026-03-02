"""
Evaluation Framework - Recall@K
"""
import json
from typing import List, Dict
from recommender import RecommendationEngine
from embeddings import EmbeddingManager


def recall_at_k(predicted: List[str], actual: List[str], k: int = 10) -> float:
    """Calculate Recall@K"""
    if not actual:
        return 0.0
    
    predicted_set = set(predicted[:k])
    actual_set = set(actual)
    
    intersection = predicted_set & actual_set
    return len(intersection) / len(actual_set)


class Evaluator:
    def __init__(self, engine: RecommendationEngine):
        self.engine = engine
    
    def load_labeled_data(self, filepath: str = "data/labeled_queries.json") -> Dict:
        """Load labeled train/test queries"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def evaluate(self, queries: List[Dict], k: int = 10) -> Dict:
        """Evaluate on labeled queries"""
        recalls = []
        results = []
        
        for query_data in queries:
            query = query_data['query']
            actual_urls = query_data['relevant_assessments']
            
            # Get recommendations
            recommendations = self.engine.recommend(query, top_k=k)
            predicted_urls = [r['url'] for r in recommendations]
            
            # Calculate recall
            recall = recall_at_k(predicted_urls, actual_urls, k)
            recalls.append(recall)
            
            results.append({
                'query': query,
                'recall@10': recall,
                'predicted': predicted_urls[:k],
                'actual': actual_urls
            })
        
        mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
        
        return {
            'mean_recall@10': mean_recall,
            'individual_results': results
        }
    
    def run_ablation_study(self, test_queries: List[Dict]) -> Dict:
        """Run ablation study to show improvements"""
        print("Running ablation study...")
        
        results = {
            'baseline': None,
            'with_reranking': None,
            'with_balancing': None
        }
        
        # Baseline: Just vector search, no reranking
        print("\n1. Baseline (vector search only)...")
        # TODO: Implement baseline version
        
        # With re-ranking
        print("\n2. With cross-encoder re-ranking...")
        # TODO: Implement
        
        # With balancing
        print("\n3. With balanced K/P filtering...")
        eval_results = self.evaluate(test_queries, k=10)
        results['with_balancing'] = eval_results['mean_recall@10']
        
        return results


def create_sample_labeled_data():
    """Create sample labeled data structure"""
    sample_data = {
        "train_queries": [
            {
                "query": "Software developer with Java and Python skills",
                "relevant_assessments": [
                    "https://www.shl.com/...",
                    "https://www.shl.com/..."
                ]
            }
        ],
        "test_queries": [
            {
                "query": "Leadership role requiring strategic thinking",
                "relevant_assessments": [
                    "https://www.shl.com/..."
                ]
            }
        ]
    }
    
    with open("data/labeled_queries.json", 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("Created sample labeled data at data/labeled_queries.json")
    print("⚠️  Replace with actual labeled data from the assignment")


if __name__ == "__main__":
    import os
    
    # Check if labeled data exists
    if not os.path.exists("data/labeled_queries.json"):
        print("No labeled data found. Creating sample structure...")
        os.makedirs("data", exist_ok=True)
        create_sample_labeled_data()
        print("\n⚠️  Please add actual labeled queries before running evaluation")
        exit(0)
    
    # Load embedding manager
    em = EmbeddingManager()
    em.load_collection()
    
    # Create engine
    engine = RecommendationEngine(em)
    
    # Create evaluator
    evaluator = Evaluator(engine)
    
    # Load data
    labeled_data = evaluator.load_labeled_data()
    
    # Evaluate on test set
    print("\n" + "="*50)
    print("EVALUATION ON TEST SET")
    print("="*50)
    
    test_results = evaluator.evaluate(labeled_data['test_queries'], k=10)
    
    print(f"\nMean Recall@10: {test_results['mean_recall@10']:.4f}")
    print("\nIndividual Results:")
    for i, result in enumerate(test_results['individual_results']):
        print(f"\nQuery {i+1}: {result['query']}")
        print(f"Recall@10: {result['recall@10']:.4f}")
    
    # Save results
    with open("data/evaluation_results.json", 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print("\n✓ Results saved to data/evaluation_results.json")
