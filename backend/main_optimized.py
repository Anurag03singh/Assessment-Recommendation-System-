"""
Memory-Optimized FastAPI Backend for 512MB Deployment
Uses pre-built ChromaDB with minimal dependencies
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import chromadb
import os
import json

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Lightweight recommendation system for SHL assessments"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
client = None
collection = None
catalog_data = None


def load_catalog():
    """Load catalog JSON for metadata"""
    global catalog_data
    if catalog_data is None:
        possible_paths = [
            "backend/data/shl_catalog.json",
            "data/shl_catalog.json",
            "./data/shl_catalog.json"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    catalog_data = json.load(f)
                print(f"✓ Loaded catalog with {len(catalog_data)} assessments")
                break
    return catalog_data


def get_collection():
    """Load pre-built ChromaDB collection"""
    global client, collection
    if collection is None:
        # Try multiple paths
        possible_paths = [
            "./chroma_db",
            "./backend/chroma_db",
            "../chroma_db"
        ]
        
        db_path = None
        for path in possible_paths:
            if os.path.exists(path):
                db_path = path
                break
        
        if not db_path:
            raise Exception("ChromaDB not found. Run embeddings.py first to build the index.")
        
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_collection("shl_assessments")
        print(f"✓ Loaded collection with {collection.count()} assessments from {db_path}")
    
    return collection


def analyze_query_simple(query: str) -> dict:
    """Simple keyword-based query analysis"""
    query_lower = query.lower()
    
    technical_keywords = [
        'java', 'python', 'sql', 'javascript', 'coding', 'programming', 
        'technical', 'software', 'numerical', 'analytical', 'developer', 'engineer'
    ]
    
    soft_keywords = [
        'communication', 'leadership', 'teamwork', 'collaboration', 
        'personality', 'behavior', 'behaviour', 'motivation'
    ]
    
    tech_score = sum(1 for kw in technical_keywords if kw in query_lower)
    soft_score = sum(1 for kw in soft_keywords if kw in query_lower)
    
    total = tech_score + soft_score
    if total == 0:
        return {'K': 0.6, 'P': 0.4}
    
    if soft_score == 0:
        return {'K': 0.7, 'P': 0.3}
    elif tech_score == 0:
        return {'K': 0.3, 'P': 0.7}
    else:
        return {'K': 0.5, 'P': 0.5}


def balance_results(results: list, weights: dict, top_k: int = 10) -> list:
    """Balance K and P type assessments"""
    k_results = []
    p_results = []
    
    for r in results:
        test_type = r['metadata'].get('test_type', '')
        if 'Knowledge & Skills' in test_type or 'Ability & Aptitude' in test_type:
            k_results.append(r)
        elif 'Personality & Behaviour' in test_type or 'Biodata' in test_type:
            p_results.append(r)
    
    k_count = int(top_k * weights['K'])
    p_count = top_k - k_count
    
    selected = k_results[:k_count] + p_results[:p_count]
    
    # Fill remaining if needed
    if len(selected) < top_k:
        remaining = [r for r in results if r not in selected]
        selected.extend(remaining[:top_k - len(selected)])
    
    return selected[:top_k]


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
        "version": "1.0-optimized"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        coll = get_collection()
        return {
            "status": "healthy",
            "assessments_count": coll.count(),
            "mode": "optimized"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
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
        # Get collection
        coll = get_collection()
        
        # Query ChromaDB - it will use stored embeddings
        # For new queries, we need embedding model which increases memory
        # Fallback: use simple text matching
        results = coll.query(
            query_texts=[query],
            n_results=min(request.top_k * 2, 20)
        )
        
        # Format results
        candidates = []
        for i in range(len(results['ids'][0])):
            candidates.append({
                'id': results['ids'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else 0
            })
        
        # Analyze query for K/P balance
        weights = analyze_query_simple(query)
        
        # Balance results
        balanced = balance_results(candidates, weights, request.top_k)
        
        # Format response
        formatted_recs = []
        for r in balanced:
            meta = r['metadata']
            test_type_list = [t.strip() for t in meta.get('test_type', '').split(',')]
            
            formatted_recs.append(RecommendedAssessment(
                url=meta.get('url', ''),
                adaptive_support=meta.get('adaptive_support', 'No'),
                description=meta.get('description', ''),
                duration=int(meta.get('duration', 60)),
                remote_support=meta.get('remote_support', 'Yes'),
                test_type=test_type_list
            ))
        
        return RecommendResponse(recommended_assessments=formatted_recs)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@app.get("/stats")
def get_stats():
    """Get system statistics"""
    try:
        coll = get_collection()
        catalog = load_catalog()
        return {
            "total_assessments": coll.count(),
            "catalog_size": len(catalog) if catalog else 0,
            "mode": "memory-optimized",
            "memory_limit": "512MB"
        }
    except Exception as e:
        return {"error": str(e)}


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# For serverless deployment (Vercel, AWS Lambda, etc.)
from mangum import Mangum
handler = Mangum(app)
