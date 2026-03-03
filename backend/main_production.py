"""
Production-Ready FastAPI Backend with Memory Optimization
Includes embedding model but with lazy loading and memory management
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import os
import json
import gc

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Production recommendation system for SHL assessments"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state - lazy loaded
_embedding_manager = None
_recommendation_engine = None


def get_engine():
    """Lazy load recommendation engine"""
    global _embedding_manager, _recommendation_engine
    
    if _recommendation_engine is None:
        # Import only when needed
        from embeddings_lite import EmbeddingManager
        from recommender import RecommendationEngine
        
        print("Initializing recommendation engine...")
        _embedding_manager = EmbeddingManager()
        
        try:
            _embedding_manager.load_collection()
            print(f"✓ Loaded existing collection with {_embedding_manager.collection.count()} assessments")
        except Exception as e:
            print(f"Building embeddings (first time setup)...")
            # Load catalog and build
            possible_paths = [
                "backend/data/shl_catalog.json",
                "data/shl_catalog.json"
            ]
            
            catalog_file = None
            for path in possible_paths:
                if os.path.exists(path):
                    catalog_file = path
                    break
            
            if catalog_file:
                with open(catalog_file, 'r', encoding='utf-8') as f:
                    assessments = json.load(f)
                _embedding_manager.build_index(assessments)
            else:
                raise Exception("Catalog file not found")
        
        _recommendation_engine = RecommendationEngine(_embedding_manager)
        
        # Force garbage collection
        gc.collect()
    
    return _recommendation_engine


# Request/Response models
class RecommendRequest(BaseModel):
    query: Optional[str] = None
    jd_url: Optional[str] = None
    jd_text: Optional[str] = None
    top_k: int = 10


class RecommendedAssessment(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]


class RecommendResponse(BaseModel):
    recommended_assessments: List[RecommendedAssessment]


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "SHL Assessment Recommender",
        "status": "running",
        "version": "1.0-production"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "production"
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    """Get assessment recommendations"""
    
    # Extract query text
    query = None
    if request.jd_url:
        try:
            response = requests.get(request.jd_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            query = soup.get_text(separator=' ', strip=True)[:5000]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    elif request.jd_text:
        query = request.jd_text
    elif request.query:
        query = request.query
    else:
        raise HTTPException(status_code=400, detail="Provide query, jd_text, or jd_url")
    
    try:
        # Get engine (lazy loaded)
        engine = get_engine()
        
        # Get recommendations
        recommendations = engine.recommend(query, top_k=request.top_k)
        
        # Format response
        formatted_recs = []
        for r in recommendations:
            formatted_recs.append(RecommendedAssessment(
                url=r['url'],
                adaptive_support=r.get('adaptive_support', 'No'),
                description=r['description'],
                duration=r.get('duration', 60),
                remote_support=r.get('remote_support', 'Yes'),
                test_type=r.get('test_type_list', [r.get('test_type', '')])
            ))
        
        # Clean up memory after request
        gc.collect()
        
        return RecommendResponse(recommended_assessments=formatted_recs)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    try:
        engine = get_engine()
        return {
            "total_assessments": engine.em.collection.count(),
            "embedding_model": "all-MiniLM-L6-v2",
            "mode": "production",
            "features": ["semantic_search", "reranking", "balanced_filtering"]
        }
    except Exception as e:
        return {"error": str(e)}


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# For serverless deployment
from mangum import Mangum
handler = Mangum(app)
