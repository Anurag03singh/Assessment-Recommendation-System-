"""
Embedding and Vector Store Management
Uses sentence-transformers for embeddings and ChromaDB for storage
"""
import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
import numpy as np


class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding model and vector store"""
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        # Initialize ChromaDB with new API
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        self.collection = None
    
    def create_enriched_text(self, assessment: Dict) -> str:
        """Create enriched text for better embedding"""
        return f"""
Assessment Name: {assessment.get('assessment_name', '')}
Test Type: {assessment.get('test_type', '')}
Description: {assessment.get('description', '')}
Skills: {assessment.get('skills', '')}
Job Level: {assessment.get('job_level', '')}
Category: {assessment.get('category', '')}
        """.strip()
    
    def build_index(self, assessments: List[Dict], collection_name: str = "shl_assessments"):
        """Build vector index from assessments"""
        print(f"Building index for {len(assessments)} assessments...")
        
        # Create or get collection
        try:
            self.client.delete_collection(collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Prepare data
        texts = [self.create_enriched_text(a) for a in assessments]
        ids = [str(i) for i in range(len(assessments))]
        metadatas = [
            {
                "assessment_name": a.get("assessment_name", ""),
                "url": a.get("url", ""),
                "test_type": a.get("test_type", "K"),
                "description": a.get("description", ""),
                "skills": a.get("skills", ""),
                "job_level": a.get("job_level", ""),
                "category": a.get("category", "")
            }
            for a in assessments
        ]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Index built with {len(assessments)} assessments")
    
    def load_collection(self, collection_name: str = "shl_assessments"):
        """Load existing collection"""
        self.collection = self.client.get_collection(collection_name)
    
    def search(self, query: str, k: int = 20) -> List[Dict]:
        """Search for similar assessments"""
        if not self.collection:
            raise ValueError("Collection not loaded. Call build_index() or load_collection() first.")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k
        )
        
        # Format results
        candidates = []
        for i in range(len(results['ids'][0])):
            candidates.append({
                'id': results['ids'][0][i],
                'metadata': results['metadatas'][0][i],
                'document': results['documents'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else 0
            })
        
        return candidates
    
    def rerank(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """Re-rank candidates using cross-encoder"""
        if not candidates:
            return []
        
        # Prepare pairs
        pairs = [[query, c['document']] for c in candidates]
        
        # Score with cross-encoder
        scores = self.cross_encoder.predict(pairs)
        
        # Add scores and sort
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(scores[i])
        
        candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        return candidates


if __name__ == "__main__":
    # Load assessments
    with open("data/shl_catalog.json", 'r', encoding='utf-8') as f:
        assessments = json.load(f)
    
    # Build index
    em = EmbeddingManager()
    em.build_index(assessments)
    
    # Test search
    results = em.search("Java developer with good communication skills", k=10)
    print("\nTop 3 results:")
    for i, r in enumerate(results[:3]):
        print(f"{i+1}. {r['metadata']['assessment_name']} ({r['metadata']['test_type']})")
