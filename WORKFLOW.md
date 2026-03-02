# Development & Deployment Workflow

## Phase 1: Data Collection (Day 1)

### Step 1: Scrape SHL Catalog
```bash
cd backend
python scraper.py
```

**Expected Output:**
- `data/shl_catalog.json` with 377+ assessments
- Each assessment has: name, URL, type (K/P), description, skills, etc.

**Validation:**
```bash
python -c "import json; data=json.load(open('data/shl_catalog.json')); print(f'Scraped {len(data)} assessments')"
```

**If < 377 assessments:**
- Website may use JavaScript rendering
- Update `scraper.py` to use Selenium
- Adjust CSS selectors based on actual HTML structure

---

## Phase 2: Build Vector Index (Day 1)

### Step 2: Generate Embeddings
```bash
python embeddings.py
```

**What happens:**
1. Loads `data/shl_catalog.json`
2. Creates enriched text for each assessment
3. Generates embeddings using `all-MiniLM-L6-v2`
4. Stores in ChromaDB at `./chroma_db/`

**Expected time:** 2-5 minutes for 377 assessments

**Validation:**
```bash
python -c "from embeddings import EmbeddingManager; em=EmbeddingManager(); em.load_collection(); print(f'Index has {em.collection.count()} embeddings')"
```

---

## Phase 3: Add Labeled Data (Day 1-2)

### Step 3: Prepare Evaluation Data

Create `data/labeled_queries.json`:
```json
{
  "train_queries": [
    {
      "query": "Software developer with Java and Python",
      "relevant_assessments": [
        "https://www.shl.com/...",
        "https://www.shl.com/..."
      ]
    }
  ],
  "test_queries": [
    {
      "query": "Leadership role requiring strategic thinking",
      "relevant_assessments": [
        "https://www.shl.com/..."
      ]
    }
  ]
}
```

**Requirements:**
- 10 train queries (for tuning)
- 9 test queries (for final evaluation)
- Each query has list of relevant assessment URLs

---

## Phase 4: Evaluation & Tuning (Day 2)

### Step 4: Run Evaluation
```bash
python evaluate.py
```

**Output:**
- Mean Recall@10 across test queries
- Individual query results
- Saved to `data/evaluation_results.json`

### Step 5: Tune Parameters

**Experiment with:**
1. Retrieval size (k=20 vs k=30)
2. K/P balance weights
3. Query enhancement strategies
4. Re-ranking thresholds

**Document improvements in TECHNICAL_DOCUMENT.md**

---

## Phase 5: API Development (Day 2-3)

### Step 6: Test API Locally
```bash
uvicorn main:app --reload
```

**Test endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Recommend
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration", "top_k": 10}'

# Stats
curl http://localhost:8000/stats
```

**Interactive docs:** http://localhost:8000/docs

---

## Phase 6: Frontend Development (Day 3)

### Step 7: Build Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

**Test:**
- Open http://localhost:3000
- Enter various queries
- Verify K/P balance
- Check result quality

---

## Phase 7: System Testing (Day 3)

### Step 8: Run Full System Test
```bash
cd backend
python test_system.py
```

**Checks:**
- ✓ Data exists and is valid
- ✓ Embeddings load correctly
- ✓ Recommender works
- ✓ API responds
- ✓ Evaluation data ready

**All tests must pass before deployment**

---

## Phase 8: Export Results (Day 3)

### Step 9: Generate Submission CSV
```bash
python export_csv.py
```

**Output:** `data/submission.csv`

**Format:**
```
Query,Assessment_url
"Java developer...",https://www.shl.com/...
"Java developer...",https://www.shl.com/...
...
```

**Expected:** 9 queries × 10 recommendations = 90 rows

---

## Phase 9: Deployment (Day 4)

### Step 10: Deploy Backend (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repo
4. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy

**Important:** Commit `chroma_db/` and `data/` to repo OR use persistent disk

### Step 11: Deploy Frontend (Vercel)

1. Import project from GitHub
2. Framework: Vite
3. Root: `frontend`
4. Build: `npm run build`
5. Output: `dist`
6. Environment: `VITE_API_URL=<backend-url>`
7. Deploy

### Step 12: Update CORS

In `backend/main.py`, update:
```python
allow_origins=["https://your-frontend.vercel.app"]
```

Redeploy backend.

---

## Phase 10: Final Submission (Day 4)

### Deliverables Checklist

- [ ] **CSV File:** `data/submission.csv` (90 rows)
- [ ] **2-Page Document:** `TECHNICAL_DOCUMENT.md`
  - Page 1: System design, architecture, data pipeline
  - Page 2: Evaluation, optimization, results
- [ ] **Deployed System:**
  - Backend URL: `https://your-api.render.com`
  - Frontend URL: `https://your-app.vercel.app`
- [ ] **GitHub Repo:** Public with README
- [ ] **Demo Video (Optional):** 2-3 min walkthrough

---

## Troubleshooting

### Issue: Scraper gets < 377 assessments
**Solution:** Use Selenium for dynamic content
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get(url)
# Wait for content to load
soup = BeautifulSoup(driver.page_source, 'html.parser')
```

### Issue: ChromaDB errors
**Solution:** Delete and rebuild
```bash
rm -rf chroma_db/
python embeddings.py
```

### Issue: Low Recall@K
**Solutions:**
1. Improve query enhancement
2. Adjust K/P weights
3. Increase retrieval size (k=30)
4. Use better embeddings (OpenAI text-embedding-3-small)

### Issue: API timeout on first request
**Cause:** Model loading
**Solution:** Add warmup request in startup event

### Issue: CORS errors
**Solution:** Update `allow_origins` in `main.py`

---

## Timeline Summary

| Day | Tasks | Deliverables |
|-----|-------|--------------|
| 1 | Scraping, indexing | shl_catalog.json, chroma_db/ |
| 2 | Evaluation, tuning | evaluation_results.json |
| 3 | API, frontend, testing | Working system |
| 4 | Deployment, submission | Live URLs, CSV, doc |

**Total:** 4 days for complete implementation
