"""
FastAPI Backend for SHL Assessment Recommendation System

This API provides endpoints for recommending SHL assessments based on job descriptions.
It uses semantic search and machine learning to match queries with relevant assessments.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import os

# Use lite version in production/low-memory environments
if os.environ.get('USE_LITE_MODE', 'false').lower() == 'true':
    from embeddings_lite import EmbeddingManager
else:
    from embeddings import EmbeddingManager

from recommender import RecommendationEngine

# Initialize FastAPI app
app = FastAPI(title="SHL Assessment Recommender API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine on startup
em = None
engine = None

def get_engine():
    """Lazy load engine - builds embeddings on first request if needed"""
    global engine, em
    if engine is None:
        # Initialize embedding manager
        if em is None:
            em = EmbeddingManager()
        
        try:
            em.load_collection()
            engine = RecommendationEngine(em)
            print("✓ Recommendation engine loaded successfully")
        except Exception as e:
            print(f"⚠️  Building embeddings (first time only, ~30 seconds)...")
            # Build embeddings if collection doesn't exist
            import json
            
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
                em.build_index(assessments)
                engine = RecommendationEngine(em)
                print("✓ Embeddings built and engine loaded")
            else:
                raise Exception("No catalog file found")
    
    return engine


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


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy"
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    """Get assessment recommendations"""
    engine = get_engine()
    
    if not engine:
        raise HTTPException(status_code=503, detail="Engine initialization failed")
    
    # Determine query source
    query = None
    
    if request.jd_url:
        # Fetch and extract text from URL
        try:
            response = requests.get(request.jd_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            query = soup.get_text(separator=' ', strip=True)
            
            # Limit length
            query = query[:5000]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    
    elif request.jd_text:
        query = request.jd_text
    
    elif request.query:
        query = request.query
    
    else:
        raise HTTPException(status_code=400, detail="Provide query, jd_text, or jd_url")
    
    # Get recommendations
    try:
        recommendations = engine.recommend(query, top_k=request.top_k)
        
        # Format according to spec
        formatted_recs = []
        for r in recommendations:
            formatted_recs.append(RecommendedAssessment(
                url=r['url'],
                adaptive_support=r.get('adaptive_support', 'No'),
                description=r['description'],
                duration=r.get('duration', 60),
                remote_support=r.get('remote_support', 'Yes'),
                test_type=r.get('test_type_list', [r['test_type']])
            ))
        
        return RecommendResponse(
            recommended_assessments=formatted_recs
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    try:
        engine = get_engine()
        if not engine or not engine.em.collection:
            return {"error": "Collection not loaded"}
        
        count = engine.em.collection.count()
        
        return {
            "total_assessments": count,
            "embedding_model": "all-MiniLM-L6-v2",
            "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# For Vercel serverless deployment
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    # Mangum not installed, skip serverless handler
    pass
