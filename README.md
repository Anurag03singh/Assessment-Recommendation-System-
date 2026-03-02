# SHL Assessment Recommendation System

Production-ready RAG-based recommendation system for SHL assessments with balanced K/P filtering and comprehensive evaluation framework.

> 🚀 **New here?** Start with **[START_HERE.md](START_HERE.md)** for a quick orientation!

## Key Features

✅ Web scraper for 377+ SHL individual test solutions  
✅ Semantic search using sentence-transformers + ChromaDB  
✅ Cross-encoder re-ranking for improved accuracy  
✅ Intelligent K/P balance based on query analysis  
✅ Recall@K evaluation framework  
✅ FastAPI backend with OpenAPI docs  
✅ Clean React + Tailwind frontend  
✅ Production deployment ready  

## Architecture

```
User Input (Query/JD/URL)
         ↓
   Preprocessing & Query Enhancement
         ↓
   Embedding (all-MiniLM-L6-v2)
         ↓
   Vector Search (ChromaDB) → Top 20
         ↓
   Cross-Encoder Re-ranking
         ↓
   Balanced K/P Filtering
         ↓
   Top 10 Recommendations
         ↓
   API Response (JSON)
```

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

```bash
# Backend (5 min)
cd backend
pip install -r requirements.txt
python setup.py  # Interactive setup
uvicorn main:app --reload

# Frontend (2 min)
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

**Note:** Sample data files are provided in `backend/data/` for testing. Replace with actual scraped data and labeled queries for production use.

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── scraper.py           # SHL catalog web scraper
│   ├── embeddings.py        # Embedding & vector store
│   ├── recommender.py       # Recommendation engine
│   ├── evaluate.py          # Recall@K evaluation
│   ├── export_csv.py        # CSV export for submission
│   ├── test_system.py       # System tests
│   ├── setup.py             # Setup wizard
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── QUICKSTART.md            # Setup guide
├── TECHNICAL_DOCUMENT.md    # 2-page technical doc
└── DEPLOYMENT.md            # Deployment guide
```

## Tech Stack

- Backend: Python 3.11, FastAPI, Sentence Transformers, ChromaDB, Cross-Encoder
- Frontend: React 18, Tailwind CSS, Vite
- Deployment: Render (API), Vercel (Frontend)
- Evaluation: Custom Recall@K implementation

## Testing

```bash
cd backend
python test_system.py  # Run all tests
```

## Documentation

📖 **[INDEX.md](INDEX.md)** - Complete documentation index and reading guide

### Getting Started
- [QUICKSTART.md](QUICKSTART.md) - Setup and usage guide (start here!)
- [COMMANDS.md](COMMANDS.md) - Command reference for all operations
- [verify_setup.py](verify_setup.py) - Verify all files are in place

### Architecture & Design
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed system architecture with diagrams
- [TECHNICAL_DOCUMENT.md](TECHNICAL_DOCUMENT.md) - 2-page technical document for submission

### Development
- [WORKFLOW.md](WORKFLOW.md) - Step-by-step development workflow
- [CHECKLIST.md](CHECKLIST.md) - Implementation checklist with time estimates
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete project overview

### Operations
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions for Render + Vercel
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## API Endpoints

- `GET /health` - Health check
- `POST /recommend` - Get recommendations
- `GET /stats` - System statistics

API docs: http://localhost:8000/docs

## Evaluation

The system achieves strong Recall@K performance through:
1. Enriched text embeddings
2. Cross-encoder re-ranking
3. Balanced K/P filtering
4. Query-aware weight adjustment

See [TECHNICAL_DOCUMENT.md](TECHNICAL_DOCUMENT.md) for detailed evaluation results.
