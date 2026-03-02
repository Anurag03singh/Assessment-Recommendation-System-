# Quick Start Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- pip and npm

## Backend Setup (5 minutes)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run setup (interactive)
python setup.py

# OR run steps manually:
python scraper.py          # Scrape SHL catalog
python embeddings.py       # Build vector index
python evaluate.py         # Run evaluation (after adding labeled data)

# Start API
uvicorn main:app --reload
```

API will be available at: http://localhost:8000

Test it: http://localhost:8000/docs

## Frontend Setup (2 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start dev server
npm run dev
```

Frontend will be available at: http://localhost:3000

## Testing the System

### 1. Test API directly

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills", "top_k": 10}'
```

### 2. Test via Frontend
- Open http://localhost:3000
- Enter query: "Need software engineer with leadership skills"
- Click "Get Recommendations"
- View balanced K/P results

### 3. Run Evaluation

```bash
cd backend

# Add your labeled queries to data/labeled_queries.json
# Then run:
python evaluate.py
```

### 4. Export CSV for Submission

```bash
cd backend
python export_csv.py
```

Output: `data/submission.csv`

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app
│   ├── scraper.py           # Web scraper
│   ├── embeddings.py        # Vector store
│   ├── recommender.py       # Recommendation engine
│   ├── evaluate.py          # Evaluation framework
│   ├── export_csv.py        # CSV export
│   ├── setup.py             # Setup script
│   ├── requirements.txt     # Python deps
│   └── data/
│       ├── shl_catalog.json
│       ├── labeled_queries.json
│       └── submission.csv
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main component
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── README.md
├── TECHNICAL_DOCUMENT.md    # 2-page doc
└── DEPLOYMENT.md
```

## Common Issues

### Scraper returns < 377 assessments
- Website may use dynamic loading (JavaScript)
- Solution: Use Selenium instead of requests
- Update scraper.py to use webdriver

### ChromaDB errors
- Delete `chroma_db/` folder and rebuild: `python embeddings.py`

### CORS errors in frontend
- Update CORS origins in `backend/main.py`
- Add your frontend URL to `allow_origins`

### Model download slow
- First run downloads sentence-transformers models (~100MB)
- Subsequent runs use cached models

## Next Steps

1. Verify scraper gets 377+ assessments
2. Add actual labeled queries from assignment
3. Run evaluation and document Recall@K
4. Deploy backend to Render
5. Deploy frontend to Vercel
6. Submit CSV + 2-page document
