"""
Minimal FastAPI Backend - No ML dependencies
Uses simple keyword matching for recommendations
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import json
import os
from collections import Counter
import re

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Lightweight recommendation system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load catalog
CATALOG = []

def load_catalog():
    global CATALOG
    possible_paths = [
        "backend/data/shl_catalog.json",
        "data/shl_catalog.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                CATALOG = json.load(f)
            print(f"✓ Loaded {len(CATALOG)} assessments")
            return
    
    print("Warning: Catalog not found")

# Load on startup
load_catalog()


def simple_recommend(query: str, top_k: int = 10):
    """Simple keyword-based recommendation"""
    query_lower = query.lower()
    
    # Extract keywords
    words = re.findall(r'\b\w+\b', query_lower)
    word_freq = Counter(words)
    
    # Score each assessment
    scored = []
    for assessment in CATALOG:
        score = 0
        text = (assessment.get('description', '') + ' ' + 
                ' '.join(assessment.get('test_type_list', []))).lower()
        
        # Count keyword matches
        for word, freq in word_freq.most_common(20):
            if len(word) > 3:  # Skip short words
                score += text.count(word) * freq
        
        scored.append((score, assessment))
    
    # Sort by score
    scored.sort(reverse=True, key=lambda x: x[0])
    
    return [item[1] for item in scored[:top_k]]


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
    return {
        "service": "SHL Assessment Recommender",
        "status": "running",
        "version": "1.0-minimal",
        "mode": "keyword-based"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "mode": "minimal",
        "assessments_loaded": len(CATALOG)
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
        # Get recommendations
        recommendations = simple_recommend(query, top_k=request.top_k)
        
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
        
        return RecommendResponse(recommended_assessments=formatted_recs)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")


@app.get("/stats")
def get_stats():
    return {
        "total_assessments": len(CATALOG),
        "mode": "keyword-based",
        "features": ["keyword_matching", "simple_scoring"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
