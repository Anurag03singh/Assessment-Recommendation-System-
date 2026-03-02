# SHL Assessment Recommendation System - Technical Documentation

## Page 1: System Design

### Problem Understanding
Build a retrieval-augmented recommendation system that:
- Crawls and structures SHL assessment catalog (377+ individual tests)
- Accepts natural language queries, full JD text, or JD URLs
- Returns balanced recommendations (K: Knowledge/Skills, P: Personality/Behavior)
- Evaluates performance using Recall@K metrics
- Provides production-ready REST API

### Architecture

```
User Input (Query/JD/URL)
         ↓
   Preprocessing Layer
   (URL fetch, text extraction, cleaning)
         ↓
   Query Enhancement
   (Extract technical vs soft skill requirements)
         ↓
   Embedding Model
   (sentence-transformers/all-MiniLM-L6-v2)
         ↓
   Vector Database (ChromaDB)
   (Cosine similarity search)
         ↓
   Initial Retrieval (Top 20)
         ↓
   Re-ranking Layer
   (Cross-Encoder: ms-marco-MiniLM-L-6-v2)
         ↓
   Balanced K/P Filtering
   (Dynamic weight allocation based on query analysis)
         ↓
   Final Top 10 Recommendations
         ↓
   API Response (JSON)
```

### Data Pipeline

**Scraping Strategy:**
- Target: https://www.shl.com/solutions/products/product-catalog/
- Tools: requests + BeautifulSoup (with Selenium fallback for dynamic content)
- Extraction: Assessment name, URL, description, skills, job level, duration, category
- Filtering: Exclude pre-packaged job solutions, focus on individual test solutions
- Classification: Rule-based K/P classification using keyword matching
- Output: Structured JSON with 377+ assessments

**Data Structure:**
```json
{
  "assessment_name": "Numerical Reasoning Test",
  "url": "https://www.shl.com/...",
  "test_type": "K",
  "description": "Measures numerical problem-solving ability",
  "skills": "Numerical, Analytical",
  "job_level": "All Levels",
  "duration": "20 min",
  "category": "Cognitive Ability"
}
```

### Embedding Strategy

**Text Enrichment:**
Instead of embedding only descriptions, we create enriched text:
```
Assessment Name: {name}
Test Type: {test_type}
Description: {description}
Skills: {skills}
Job Level: {job_level}
Category: {category}
```

This improves semantic matching by providing richer context.

**Model Selection:**
- Embedding: `all-MiniLM-L6-v2` (384 dimensions, fast, good quality)
- Re-ranker: `cross-encoder/ms-marco-MiniLM-L-6-v2` (higher accuracy)
- Vector DB: ChromaDB with cosine similarity

### Retrieval Pipeline

**Stage 1: Vector Search**
- Encode query using embedding model
- Retrieve top 20 candidates from ChromaDB
- Fast but coarse-grained matching

**Stage 2: Cross-Encoder Re-ranking**
- Compute query-document similarity scores
- More accurate than bi-encoder embeddings
- Sort by re-ranking score

**Stage 3: Balanced Filtering**
Query analysis determines K/P weights:
- Technical-heavy query → 70% K, 30% P
- Soft-skill-heavy query → 30% K, 70% P
- Balanced query → 50% K, 50% P

Algorithm:
1. Separate candidates by test_type (K vs P)
2. Calculate target counts: k_count = top_k × weight_K
3. Select top k_count from K candidates, p_count from P candidates
4. Fill remaining slots if one category is insufficient
5. Sort final selection by re-ranking score

---

## Page 2: Optimization & Evaluation

### Baseline Method
Simple vector search with no re-ranking or balancing:
- Embed query
- Retrieve top 10 from ChromaDB
- Return results as-is

### Experiments & Improvements

**Experiment 1: Enhanced Text Representation**
- Baseline: Embed description only
- Improved: Embed enriched text (name + type + description + skills + category)
- Impact: Better semantic matching, especially for skill-specific queries

**Experiment 2: Cross-Encoder Re-ranking**
- Added: ms-marco-MiniLM-L-6-v2 cross-encoder after initial retrieval
- Retrieve top 20, re-rank to top 10
- Impact: Improved relevance of top results

**Experiment 3: Query Analysis & Balancing**
- Analyze query for technical vs soft skill keywords
- Dynamically adjust K/P ratio
- Enforce balanced recommendations
- Impact: Better alignment with job requirements

**Experiment 4: Query Enhancement (Optional)**
- Use LLM to extract structured requirements from free-text queries
- Convert to: {technical_skills: [...], soft_skills: [...], level: "..."}
- Impact: More precise retrieval for ambiguous queries

### Evaluation Metrics

**Recall@K Formula:**
```
Recall@K = |Predicted ∩ Actual| / |Actual|
```

**Evaluation Process:**
1. Load labeled queries (10 train, 9 test)
2. For each query:
   - Generate top 10 recommendations
   - Compare with ground truth
   - Calculate Recall@10
3. Compute mean across all queries

**Expected Results:**
| Version | Mean Recall@10 |
|---------|----------------|
| Baseline (vector only) | 0.42 |
| + Enriched embeddings | 0.55 |
| + Cross-encoder | 0.68 |
| + Balanced filtering | 0.75+ |

### Performance Optimization

**Indexing:**
- Pre-compute embeddings offline
- Store in ChromaDB with HNSW index
- Query time: <100ms for top 20 retrieval

**Caching:**
- Cache frequent queries
- Cache cross-encoder scores for common pairs

**Scalability:**
- Current: 377 assessments, in-memory ChromaDB
- Scale: Move to persistent ChromaDB or Pinecone for 10K+ assessments
- API: Add rate limiting, async processing for batch requests

### Future Improvements

1. **LLM-based Query Enhancement:** Use GPT/Gemini to extract structured requirements
2. **User Feedback Loop:** Collect clicks/ratings to fine-tune ranking
3. **Hybrid Search:** Combine semantic + keyword search (BM25)
4. **Multi-stage Filtering:** Add job level, duration, category filters
5. **Explainability:** Show why each assessment was recommended
6. **A/B Testing:** Compare different balancing strategies

### API Design

**Endpoints:**
- `GET /health` - Health check
- `POST /recommend` - Get recommendations
- `GET /stats` - System statistics

**Request Format:**
```json
{
  "query": "Java developer with collaboration skills",
  "jd_url": "https://...",
  "jd_text": "...",
  "top_k": 10
}
```

**Response Format:**
```json
{
  "recommendations": [
    {
      "assessment_name": "...",
      "url": "...",
      "test_type": "K",
      "description": "...",
      "skills": "...",
      "category": "..."
    }
  ],
  "query_used": "...",
  "k_count": 6,
  "p_count": 4
}
```

### Tech Stack Summary
- Backend: Python, FastAPI, Sentence Transformers, ChromaDB
- Frontend: React, Tailwind, Vite
- Deployment: Render (API), Vercel (Frontend)
- Evaluation: Custom Recall@K implementation
