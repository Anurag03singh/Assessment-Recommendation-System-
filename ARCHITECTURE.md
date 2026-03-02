# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (Vercel)                     │  │
│  │  • Query Input                                           │  │
│  │  • JD URL Input                                          │  │
│  │  • Results Display                                       │  │
│  │  • K/P Balance Visualization                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/JSON
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   /health    │  │  /recommend  │  │    /stats    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RECOMMENDATION ENGINE                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Query Analysis                                       │  │
│  │     • Detect technical vs soft skills                    │  │
│  │     • Calculate K/P weights                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Query Enhancement (Optional)                         │  │
│  │     • Extract structured requirements                    │  │
│  │     • Expand with synonyms                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Vector Search                                        │  │
│  │     • Generate query embedding                           │  │
│  │     • Search ChromaDB (Top 20)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Re-ranking                                           │  │
│  │     • Cross-encoder scoring                              │  │
│  │     • Sort by relevance                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  5. Balanced Filtering                                   │  │
│  │     • Apply K/P weights                                  │  │
│  │     • Select top K from each category                    │  │
│  │     • Return Top 10                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA & MODELS                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  ChromaDB    │  │  Embeddings  │  │ Cross-Encoder│        │
│  │  Vector DB   │  │  all-MiniLM  │  │  ms-marco    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SHL Catalog (377+ Assessments)                         │  │
│  │  • Assessment metadata                                   │  │
│  │  • K/P classification                                    │  │
│  │  • Skills, levels, categories                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Data Collection Pipeline

```
SHL Website
    │
    │ Web Scraping
    │ (BeautifulSoup/Selenium)
    ▼
Raw HTML
    │
    │ Parsing & Extraction
    ▼
Structured Data
    │
    │ K/P Classification
    │ Metadata Enrichment
    ▼
shl_catalog.json
(377+ assessments)
```

### 2. Indexing Pipeline

```
shl_catalog.json
    │
    │ For each assessment:
    ▼
Enriched Text Creation
    │
    │ "Assessment: {name}
    │  Type: {type}
    │  Description: {desc}
    │  Skills: {skills}
    │  Level: {level}
    │  Category: {category}"
    ▼
Embedding Generation
(all-MiniLM-L6-v2)
    │
    │ 384-dim vectors
    ▼
ChromaDB Storage
(with metadata)
```

### 3. Query Processing Pipeline

```
User Input
    │
    ├─ Text Query
    ├─ JD URL ──→ Fetch & Extract
    └─ JD Text
    │
    ▼
Query Analysis
    │
    ├─ Technical keywords → K weight
    └─ Soft skill keywords → P weight
    │
    ▼
Enhanced Query
    │
    │ Generate embedding
    ▼
Query Vector
(384-dim)
```

### 4. Retrieval Pipeline

```
Query Vector
    │
    │ Cosine Similarity Search
    ▼
ChromaDB
    │
    │ Top 20 candidates
    ▼
Initial Results
    │
    │ Cross-Encoder Re-ranking
    │ (query, document) → score
    ▼
Re-ranked Results
    │
    │ Balanced K/P Filtering
    │ • Separate by type
    │ • Apply weights
    │ • Select top from each
    ▼
Final Top 10
Recommendations
```

## Component Architecture

### Backend Components

```
main.py (FastAPI App)
    │
    ├─ /health ──────────────→ Health Check
    │
    ├─ /recommend ───────────→ recommender.py
    │                              │
    │                              ├─ Query Analysis
    │                              ├─ embeddings.py
    │                              │     │
    │                              │     ├─ Vector Search
    │                              │     └─ Re-ranking
    │                              │
    │                              └─ Balanced Filtering
    │
    └─ /stats ───────────────→ System Statistics
```

### Frontend Components

```
App.jsx
    │
    ├─ Query Input Form
    │     │
    │     ├─ Text Area (query)
    │     └─ URL Input (jd_url)
    │
    ├─ Submit Handler
    │     │
    │     └─ POST /recommend
    │
    └─ Results Display
          │
          ├─ K/P Balance Badge
          └─ Assessment Cards
                │
                ├─ Name & Type
                ├─ Description
                ├─ Skills & Category
                └─ Link to SHL
```

## Evaluation Architecture

```
Labeled Queries
(train + test)
    │
    ▼
Recommendation Engine
    │
    ├─ Generate predictions
    │
    ▼
Predicted URLs
    │
    │ Compare with ground truth
    ▼
Recall@K Calculation
    │
    │ For each query:
    │ recall = |predicted ∩ actual| / |actual|
    │
    ▼
Mean Recall@10
    │
    └─ evaluation_results.json
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         PRODUCTION                          │
│                                                             │
│  ┌──────────────────────┐         ┌──────────────────────┐ │
│  │   Vercel (Frontend)  │         │  Render (Backend)    │ │
│  │                      │         │                      │ │
│  │  • React App         │◄────────┤  • FastAPI           │ │
│  │  • Static Assets     │  HTTPS  │  • Python Runtime    │ │
│  │  • CDN Distribution  │         │  • ChromaDB          │ │
│  │                      │         │  • Models            │ │
│  └──────────────────────┘         └──────────────────────┘ │
│           │                                  │              │
│           │                                  │              │
│           ▼                                  ▼              │
│  ┌──────────────────────┐         ┌──────────────────────┐ │
│  │  Users (Browser)     │         │  Persistent Storage  │ │
│  └──────────────────────┘         │  • chroma_db/        │ │
│                                    │  • data/             │ │
│                                    └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  React 18 • Tailwind CSS • Vite                            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                              │
│  FastAPI • Uvicorn • Pydantic                              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                      │
│  Recommendation Engine • Query Analysis • Filtering         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      ML/NLP LAYER                           │
│  Sentence Transformers • Cross-Encoder • Embeddings         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                             │
│  ChromaDB • JSON Files • Vector Storage                     │
└─────────────────────────────────────────────────────────────┘
```

## Scalability Considerations

### Current Architecture (377 assessments)
- In-memory ChromaDB
- Single server deployment
- Synchronous processing
- ~100ms query time

### Scaled Architecture (10K+ assessments)
```
Load Balancer
    │
    ├─ API Server 1 ──┐
    ├─ API Server 2 ──┼──→ Managed ChromaDB / Pinecone
    └─ API Server 3 ──┘         │
                                └──→ Persistent Vector Store
                                
    Redis Cache ──→ Frequent queries
    
    Async Workers ──→ Batch processing
```

## Security Architecture

```
User Request
    │
    ▼
HTTPS/TLS
    │
    ▼
CORS Validation
    │
    ▼
Rate Limiting
    │
    ▼
Input Validation
(Pydantic)
    │
    ▼
Business Logic
    │
    ▼
Response
```

## Monitoring & Observability

```
Application
    │
    ├─ Logs ──────────→ Structured Logging
    │
    ├─ Metrics ───────→ Response Time, Recall@K
    │
    ├─ Errors ────────→ Exception Tracking
    │
    └─ Health ────────→ /health endpoint
```

## Key Design Decisions

1. **ChromaDB over FAISS**
   - Easier metadata filtering
   - Built-in persistence
   - Better developer experience

2. **Cross-Encoder Re-ranking**
   - Higher accuracy than bi-encoder alone
   - Acceptable latency for top-20 candidates
   - Significant Recall@K improvement

3. **Balanced K/P Filtering**
   - Ensures diverse recommendations
   - Aligns with job requirements
   - Prevents type bias

4. **FastAPI over Flask**
   - Automatic OpenAPI docs
   - Type validation with Pydantic
   - Better async support
   - Modern Python features

5. **React + Vite over CRA**
   - Faster build times
   - Smaller bundle size
   - Better developer experience
   - Modern tooling
