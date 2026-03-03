"""
Lightweight Embedding Manager for Memory-Constrained Environments
Uses smaller models and lazy loading to reduce memory footprint
"""
import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
import os


class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", db_path: str = "./chroma_db"):
        """Initialize with lazy loading - models loaded on first use"""
        self.model_name = model_name
        self.db_path = db_path
        self._embedding_model = None
        self._cross_encoder = None
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = None
    
    @property
    def embedding_model(self):
        """Lazy load embedding model"""
        if self._embedding_model is None:
            print(f"Loading embedding model: {self.model_name}")
            self._embedding_model = SentenceTransformer(self.model_name)
        return self._embedding_model
    
    @property
    def cross_encoder(self):
        """Lazy load cross encoder - only when needed for reranking"""
        if self._cross_encoder is None:
            print("Loading cross-encoder for reranking...")
            from sentence_transformers import CrossEncoder
            self._cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        return self._cross_encoder
    
    def create_enriched_text(self, assessment: Dict) -> str:
        """Create enriched text for better embedding"""
        test_types = ", ".join(assessment.get('test_type', []))
        return f"""
Assessment Name: {assessment.get('assessment_name', '')}
Test Type: {test_types}
Description: {assessment.get('description', '')}
Duration: {assessment.get('duration', '')} minutes
Adaptive Support: {assessment.get('adaptive_support', 'No')}
Remote Support: {assessment.get('remote_support', 'Yes')}
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
                "test_type": ", ".join(a.get("test_type", [])),
                "description": a.get("description", ""),
                "duration": a.get("duration", 60),
                "adaptive_support": a.get("adaptive_support", "No"),
                "remote_support": a.get("remote_support", "Yes")
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
        """Re-rank candidates using cross-encoder (optional, uses more memory)"""
        if not candidates:
            return []
        
        # Skip reranking in low-memory environments
        if os.environ.get('SKIP_RERANKING', 'false').lower() == 'true':
            print("Skipping reranking (SKIP_RERANKING=true)")
            return candidates
        
        # Prepare pairs
        pairs = [[query, c['document']] for c in candidates]
        
        # Score with cross-encoder
        scores = self.cross_encoder.predict(pairs)
        
        # Add scores and sort
        for i, candidate in enumerate(candidates):
            candidate['rerank_score'] = float(scores[i])
        
        candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        return candidates
