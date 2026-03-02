"""
FastAPI Backend for SHL Assessment Recommendation System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from embeddings import EmbeddingManager
from recommender import RecommendationEngine

app = FastAPI(title="SHL Assessment Recommender API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engine
em = EmbeddingManager()
try:
    em.load_collection()
    engine = RecommendationEngine(em)
    print("✓ Recommendation engine loaded")
except Exception as e:
    print(f"⚠️  Warning: Could not load collection: {e}")
    print("Run 'python embeddings.py' to build the index first")
    engine = None


class RecommendRequest(BaseModel):
    query: Optional[str] = None
    jd_url: Optional[str] = None
    jd_text: Optional[str] = None
    top_k: int = 10


class Assessment(BaseModel):
    assessment_name: str
    url: str
    test_type: str
    description: str
    skills: str
    category: str


class RecommendResponse(BaseModel):
    recommendations: List[Assessment]
    query_used: str
    k_count: int
    p_count: int


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "engine_loaded": engine is not None
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    """Get assessment recommendations"""
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not initialized. Build index first.")
    
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
        
        # Count K vs P
        k_count = sum(1 for r in recommendations if r['test_type'] == 'K')
        p_count = len(recommendations) - k_count
        
        return RecommendResponse(
            recommendations=[Assessment(**r) for r in recommendations],
            query_used=query[:200] + "..." if len(query) > 200 else query,
            k_count=k_count,
            p_count=p_count
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    if not engine or not engine.em.collection:
        return {"error": "Collection not loaded"}
    
    count = engine.em.collection.count()
    
    return {
        "total_assessments": count,
        "embedding_model": "all-MiniLM-L6-v2",
        "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
