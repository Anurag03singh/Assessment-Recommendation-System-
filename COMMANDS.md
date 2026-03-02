# Command Reference

Quick reference for all commands used in this project.

## Setup & Verification

```bash
# Verify all files are present
python verify_setup.py

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
```

## Backend Commands

### Quick Testing (with sample data)
```bash
cd backend
python quick_test.py
```

### Data Collection
```bash
# Scrape SHL catalog (377+ assessments)
python scraper.py

# Check scraped data
python -c "import json; data=json.load(open('data/shl_catalog.json')); print(f'Scraped {len(data)} assessments')"
```

### Indexing
```bash
# Build vector index
python embeddings.py

# Verify index
python -c "from embeddings import EmbeddingManager; em=EmbeddingManager(); em.load_collection(); print(f'Index: {em.collection.count()} embeddings')"
```

### Evaluation
```bash
# Run evaluation (requires labeled data)
python evaluate.py

# View results
cat data/evaluation_results.json
```

### Testing
```bash
# Run system tests
python test_system.py

# Run setup wizard
python setup.py
```

### API Server
```bash
# Start development server
uvicorn main:app --reload

# Start production server
uvicorn main:app --host 0.0.0.0 --port 8000

# With custom port
uvicorn main:app --port 8080
```

### Export
```bash
# Export CSV for submission
python export_csv.py

# View CSV
cat data/submission.csv
```

## Frontend Commands

### Development
```bash
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Setup
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# For production
echo "VITE_API_URL=https://your-api.render.com" > .env
```

## API Testing

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Get recommendations (query)
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills", "top_k": 10}'

# Get recommendations (JD URL)
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"jd_url": "https://example.com/job-posting", "top_k": 10}'

# Get statistics
curl http://localhost:8000/stats

# Interactive API docs
# Open: http://localhost:8000/docs
```

### Using Python requests

```python
import requests

# Recommend
response = requests.post(
    'http://localhost:8000/recommend',
    json={'query': 'Java developer', 'top_k': 10}
)
print(response.json())
```

## Docker Commands

```bash
# Build image
cd backend
docker build -t shl-recommender .

# Run container
docker run -p 8000:8000 shl-recommender

# Run with volume (for data persistence)
docker run -p 8000:8000 -v $(pwd)/data:/app/data -v $(pwd)/chroma_db:/app/chroma_db shl-recommender
```

## Git Commands

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit: SHL Assessment Recommender"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/shl-recommender.git
git branch -M main
git push -u origin main

# Update after changes
git add .
git commit -m "Update: description of changes"
git push
```

## Deployment Commands

### Render (Backend)

```bash
# Build command (set in Render dashboard)
pip install -r requirements.txt

# Start command (set in Render dashboard)
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Vercel (Frontend)

```bash
# Install Vercel CLI (optional)
npm install -g vercel

# Deploy from CLI
cd frontend
vercel

# Or use Vercel dashboard to import from GitHub
```

## Data Management

```bash
# View catalog
cat backend/data/shl_catalog.json | python -m json.tool | less

# Count assessments
python -c "import json; print(len(json.load(open('backend/data/shl_catalog.json'))))"

# Check K vs P distribution
python -c "import json; data=json.load(open('backend/data/shl_catalog.json')); k=sum(1 for d in data if d['test_type']=='K'); print(f'K: {k}, P: {len(data)-k}')"

# View labeled queries
cat backend/data/labeled_queries.json | python -m json.tool

# View evaluation results
cat backend/data/evaluation_results.json | python -m json.tool
```

## Troubleshooting Commands

```bash
# Check Python version
python --version

# Check Node version
node --version

# Check installed packages
pip list
npm list

# Clear ChromaDB and rebuild
rm -rf backend/chroma_db
cd backend
python embeddings.py

# Check if API is running
curl http://localhost:8000/health

# Check if port is in use (Windows)
netstat -ano | findstr :8000

# Check if port is in use (Linux/Mac)
lsof -i :8000

# Kill process on port (Windows)
# Find PID from netstat, then:
taskkill /PID <PID> /F

# Kill process on port (Linux/Mac)
kill -9 $(lsof -t -i:8000)
```

## Performance Testing

```bash
# Time API response
time curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer", "top_k": 10}'

# Load test with Apache Bench (if installed)
ab -n 100 -c 10 -p query.json -T application/json http://localhost:8000/recommend

# query.json content:
# {"query": "Java developer", "top_k": 10}
```

## Useful One-Liners

```bash
# Count lines of code
find . -name "*.py" -o -name "*.jsx" | xargs wc -l

# Find TODO comments
grep -r "TODO" backend/ frontend/

# Check for print statements (should use logging)
grep -r "print(" backend/*.py

# List all API endpoints
python -c "from backend.main import app; print([route.path for route in app.routes])"

# Get model size
du -sh backend/chroma_db/

# Check data quality
python -c "import json; data=json.load(open('backend/data/shl_catalog.json')); missing=[d['assessment_name'] for d in data if not d.get('url')]; print(f'Missing URLs: {len(missing)}')"
```

## Environment Variables

```bash
# Backend (optional)
export OPENAI_API_KEY=your_key_here  # If using OpenAI embeddings
export GEMINI_API_KEY=your_key_here  # If using Gemini

# Frontend
export VITE_API_URL=http://localhost:8000
```

## Cleanup Commands

```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove node_modules
rm -rf frontend/node_modules

# Remove build artifacts
rm -rf frontend/dist

# Remove ChromaDB
rm -rf backend/chroma_db

# Full cleanup (keep source code only)
rm -rf backend/__pycache__ backend/chroma_db backend/data/*.json
rm -rf frontend/node_modules frontend/dist
```

## Quick Workflows

### First Time Setup
```bash
python verify_setup.py
cd backend && pip install -r requirements.txt
python quick_test.py
uvicorn main:app --reload
# In new terminal:
cd frontend && npm install && npm run dev
```

### Daily Development
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Testing
cd backend
python test_system.py
```

### Before Deployment
```bash
cd backend
python test_system.py
python evaluate.py
python export_csv.py
cd ../frontend
npm run build
```

### Full Pipeline
```bash
cd backend
python scraper.py          # 1. Scrape data
python embeddings.py       # 2. Build index
python evaluate.py         # 3. Evaluate
python export_csv.py       # 4. Export CSV
uvicorn main:app --reload  # 5. Start API
```
