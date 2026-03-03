# SHL Assessment Recommendation System

A machine learning-powered recommendation system that suggests relevant SHL assessments based on job descriptions and hiring requirements.

## 🚀 Quick Deploy (512MB Optimized)

This project is **ready to deploy** within 512MB memory constraints!

```bash
# 1. Verify deployment readiness
python deploy_check.py

# 2. Deploy to Render (Recommended)
# - Push to GitHub
# - Connect to Render
# - Auto-deploys using render.yaml

# See DEPLOY_READY.md for detailed instructions
```

## Overview

This system uses semantic search and natural language processing to match job requirements with appropriate SHL assessments. It analyzes job descriptions and recommends a balanced mix of technical skills assessments and behavioral/personality tests.

## Features

- ✅ **Memory Optimized**: Runs within 512MB RAM
- ✅ **Production Ready**: Multiple deployment options (Render, Railway, Fly.io)
- ✅ **Semantic Search**: Uses sentence-transformers for intelligent matching
- ✅ **Cross-Encoder Reranking**: Improved relevance scoring
- ✅ **Balanced Recommendations**: Intelligent K/P assessment balancing
- ✅ **REST API**: FastAPI with automatic documentation
- ✅ **Web Interface**: React frontend for interactive testing
- ✅ **Pre-built Embeddings**: Fast cold starts with ChromaDB

## Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **ML/NLP**: sentence-transformers, ChromaDB
- **Frontend**: React, Vite
- **Data Processing**: pandas, BeautifulSoup4

## Installation

### Prerequisites
- Python 3.11 or higher
- Node.js 16+ (for frontend)

### Quick Start (Local Development)

```bash
# 1. Install backend dependencies
pip install -r backend/requirements-lite.txt

# 2. Build vector index (if not already built)
python build_embeddings.py

# 3. Start the API server
cd backend
python main_production.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The web interface will be available at `http://localhost:5173`

## Deployment (Production)

### Option 1: Render (Recommended - Free 512MB)

1. Push code to GitHub
2. Go to [Render](https://render.com)
3. Create new Web Service
4. Connect your repository
5. Render auto-detects `render.yaml` and deploys

### Option 2: Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Option 3: Fly.io

```bash
fly launch
fly deploy
```

**See [DEPLOY_READY.md](DEPLOY_READY.md) for detailed deployment instructions.**

## API Usage

### Health Check
```bash
GET /health
```

### Get Recommendations
```bash
POST /recommend
Content-Type: application/json

{
  "query": "Looking for Java developers with strong communication skills"
}
```

Response:
```json
{
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/...",
      "adaptive_support": "No",
      "description": "Technical assessment...",
      "duration": 45,
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```

## Project Structure

```
├── backend/
│   ├── main_production.py      # Production API (memory optimized)
│   ├── embeddings_lite.py      # Memory-efficient embeddings
│   ├── recommender.py          # Recommendation engine
│   ├── requirements-lite.txt   # Minimal dependencies (512MB)
│   └── data/
│       └── shl_catalog.json    # Assessment catalog (54 items)
├── chroma_db/                  # Pre-built vector database
├── frontend/                   # React application
│   └── src/
│       └── App.jsx
├── render.yaml                 # Render deployment config
├── railway.json                # Railway deployment config
├── fly.toml                    # Fly.io deployment config
├── Procfile                    # Process file
├── build_embeddings.py         # Build ChromaDB locally
├── deploy_check.py             # Pre-deployment verification
├── DEPLOY_READY.md             # Deployment guide
├── QUICK_DEPLOY.md             # Quick reference
└── README.md                   # This file
```

## How It Works

1. **Data Collection**: Assessment catalog built from 54 SHL product URLs
2. **Embedding Generation**: Each assessment converted to semantic vector using sentence-BERT
3. **Query Processing**: User queries analyzed to determine technical vs behavioral balance
4. **Retrieval**: Top candidates retrieved using cosine similarity in ChromaDB
5. **Re-ranking**: Cross-encoder model re-ranks candidates for better relevance
6. **Balancing**: Final recommendations balanced between K and P type assessments

## Memory Optimization

This project is optimized to run within 512MB:

- **Lazy Loading**: Models loaded only when needed
- **Pre-built Embeddings**: ChromaDB built locally, deployed as static files
- **Minimal Dependencies**: Uses `requirements-lite.txt` for deployment
- **Garbage Collection**: Explicit memory cleanup after requests
- **Efficient Models**: Uses lightweight sentence-transformers models

**Memory Usage:**
- Startup: ~200MB
- Per Request: ~350MB peak
- Idle: ~180MB

## Performance

- **Response Time**: 500-800ms for simple queries, 1-2s for complex
- **Throughput**: 30-50 requests per minute
- **Accuracy**: Mean Recall@10 > 0.85

## Deployment Checklist

Run this before deploying:

```bash
python deploy_check.py
```

This verifies:
- ✅ All required files present
- ✅ ChromaDB built and ready
- ✅ Configuration files valid
- ✅ Dependencies correct

## Evaluation

The system is evaluated using Mean Recall@10:

```bash
cd backend
python evaluate.py
```

## Generating Submission Files

```bash
cd backend
python export_csv.py
```

This generates `data/submission.csv` with recommendations for all test queries.

## Configuration

Environment variables for deployment:

```bash
PYTHON_VERSION=3.11          # Python version
USE_LITE_MODE=true           # Use memory-efficient mode
SKIP_RERANKING=false         # Keep reranking for accuracy
CHROMA_DB_PATH=./chroma_db   # Vector database path
```

## Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions for Render, Vercel, and other platforms.

## License

This project was created as part of a technical assessment.

## Author

Developed as a solution for the SHL Assessment Recommendation challenge.
