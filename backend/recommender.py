"""
Recommendation Engine with Balanced K/P Logic
"""
from typing import List, Dict, Optional
from embeddings import EmbeddingManager
import re


class RecommendationEngine:
    def __init__(self, embedding_manager: EmbeddingManager):
        self.em = embedding_manager
        
        # Keywords for query analysis
        self.technical_keywords = [
            'java', 'python', 'coding', 'programming', 'technical', 'software',
            'numerical', 'analytical', 'problem solving', 'cognitive', 'aptitude',
            'skill', 'ability', 'knowledge', 'competency'
        ]
        
        self.soft_keywords = [
            'communication', 'leadership', 'teamwork', 'collaboration', 'personality',
            'behavior', 'motivation', 'culture', 'interpersonal', 'emotional',
            'adaptability', 'resilience', 'integrity'
        ]
    
    def analyze_query(self, query: str) -> Dict[str, float]:
        """Analyze query to determine K vs P weight"""
        query_lower = query.lower()
        
        technical_score = sum(1 for kw in self.technical_keywords if kw in query_lower)
        soft_score = sum(1 for kw in self.soft_keywords if kw in query_lower)
        
        total = technical_score + soft_score
        
        if total == 0:
            # Default: balanced
            return {'K': 0.6, 'P': 0.4}
        
        # Calculate weights
        if soft_score == 0:
            return {'K': 0.7, 'P': 0.3}
        elif technical_score == 0:
            return {'K': 0.3, 'P': 0.7}
        else:
            # Both present: aim for balance
            return {'K': 0.5, 'P': 0.5}
    
    def apply_balanced_filtering(self, candidates: List[Dict], weights: Dict[str, float], 
                                  top_k: int = 10) -> List[Dict]:
        """Apply balanced K/P filtering"""
        # Separate by type
        k_candidates = [c for c in candidates if c['metadata']['test_type'] == 'K']
        p_candidates = [c for c in candidates if c['metadata']['test_type'] == 'P']
        
        # Calculate target counts
        k_count = int(top_k * weights['K'])
        p_count = top_k - k_count
        
        # Select top from each category
        selected = []
        selected.extend(k_candidates[:k_count])
        selected.extend(p_candidates[:p_count])
        
        # If one category doesn't have enough, fill from the other
        if len(selected) < top_k:
            remaining = top_k - len(selected)
            all_remaining = [c for c in candidates if c not in selected]
            selected.extend(all_remaining[:remaining])
        
        # Sort by rerank score
        selected.sort(key=lambda x: x.get('rerank_score', 0), reverse=True)
        
        return selected[:top_k]
    
    def enhance_query(self, query: str) -> str:
        """Enhance query for better retrieval (optional LLM step)"""
        # Simple rule-based enhancement
        # In production, use LLM to extract structured requirements
        return query
    
    def recommend(self, query: str, top_k: int = 10, 
                  retrieve_k: int = 20) -> List[Dict]:
        """Main recommendation pipeline"""
        # Step 1: Enhance query
        enhanced_query = self.enhance_query(query)
        
        # Step 2: Analyze query for K/P balance
        weights = self.analyze_query(enhanced_query)
        
        # Step 3: Retrieve top candidates
        candidates = self.em.search(enhanced_query, k=retrieve_k)
        
        # Step 4: Re-rank
        candidates = self.em.rerank(enhanced_query, candidates)
        
        # Step 5: Apply balanced filtering
        recommendations = self.apply_balanced_filtering(candidates, weights, top_k)
        
        # Format output
        results = []
        for rec in recommendations:
            results.append({
                'assessment_name': rec['metadata']['assessment_name'],
                'url': rec['metadata']['url'],
                'test_type': rec['metadata']['test_type'],
                'description': rec['metadata']['description'],
                'skills': rec['metadata']['skills'],
                'category': rec['metadata']['category'],
                'score': rec.get('rerank_score', 0)
            })
        
        return results


if __name__ == "__main__":
    # Test
    em = EmbeddingManager()
    em.load_collection()
    
    engine = RecommendationEngine(em)
    
    test_query = "Need Java developer with good collaboration skills"
    results = engine.recommend(test_query, top_k=10)
    
    print(f"\nQuery: {test_query}")
    print(f"\nTop 10 Recommendations:")
    for i, r in enumerate(results):
        print(f"{i+1}. {r['assessment_name']} ({r['test_type']}) - Score: {r['score']:.3f}")
