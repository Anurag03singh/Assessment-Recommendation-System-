"""
Minimal FastAPI Backend - Uses pre-built embeddings only
No model loading, just ChromaDB queries
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import chromadb
import os

app = FastAPI(title="SHL Assessment Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ChromaDB client
client = None
collection = None


def get_collection():
    """Load pre-built ChromaDB collection"""
    global client, collection
    if collection is None:
        db_path = os.environ.get('CHROMA_DB_PATH', './chroma_db')
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_collection("shl_assessments")
        print(f"✓ Loaded collection with {collection.count()} assessments")
    return collection


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
    try:
        coll = get_collection()
        return {
            "status": "healthy",
            "assessments_count": coll.count()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    """Get assessment recommendations using pre-built embeddings"""
    
    # Get query text
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
    
    # Search using ChromaDB's built-in query (uses pre-computed embeddings)
    try:
        coll = get_collection()
        
        # ChromaDB can search by text directly if embeddings are pre-built
        # But we need the embedding model for new queries...
        # This is the limitation - we need sentence-transformers
        
        # For now, return error message
        raise HTTPException(
            status_code=501,
            detail="This minimal version requires embedding model. Use full version or upgrade Vercel plan."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    try:
        coll = get_collection()
        return {
            "total_assessments": coll.count(),
            "mode": "minimal (pre-built embeddings only)"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# For Vercel
from mangum import Mangum
handler = Mangum(app)
