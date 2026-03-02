# Troubleshooting Guide

Common issues and their solutions.

## Setup Issues

### Issue: `pip install` fails with dependency conflicts

**Symptoms:**
```
ERROR: Cannot install package X because it conflicts with package Y
```

**Solutions:**
1. Use a virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
```

2. Update pip:
```bash
python -m pip install --upgrade pip
```

3. Install specific versions:
```bash
pip install -r requirements.txt --no-cache-dir
```

---

### Issue: `npm install` fails

**Symptoms:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solutions:**
1. Clear npm cache:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

2. Use legacy peer deps:
```bash
npm install --legacy-peer-deps
```

3. Update Node.js to latest LTS version

---

## Scraping Issues

### Issue: Scraper returns < 377 assessments

**Symptoms:**
```
Scraped 45 assessments
⚠️  WARNING: Only scraped 45 assessments
```

**Causes:**
- Website uses JavaScript rendering
- CSS selectors don't match current HTML structure
- Rate limiting or blocking

**Solutions:**

1. **Use Selenium for dynamic content:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get(url)

# Wait for content to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "assessment-card")))

soup = BeautifulSoup(driver.page_source, 'html.parser')
```

2. **Inspect actual HTML structure:**
- Open https://www.shl.com/solutions/products/product-catalog/ in browser
- Right-click → Inspect
- Find assessment elements
- Update CSS selectors in `scraper.py`

3. **Add delays to avoid rate limiting:**
```python
import time
time.sleep(2)  # Wait 2 seconds between requests
```

4. **Use sample data for testing:**
```bash
python quick_test.py  # Uses sample_catalog.json
```

---

### Issue: Scraper gets blocked (403/429 errors)

**Symptoms:**
```
requests.exceptions.HTTPError: 403 Forbidden
```

**Solutions:**
1. Add proper User-Agent:
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

2. Add delays between requests:
```python
time.sleep(random.uniform(1, 3))
```

3. Use rotating proxies (if necessary)

---

## Embedding & Index Issues

### Issue: ChromaDB errors on first run

**Symptoms:**
```
chromadb.errors.InvalidCollectionException
```

**Solutions:**
1. Delete and rebuild:
```bash
rm -rf chroma_db/
python embeddings.py
```

2. Check disk space:
```bash
df -h  # Linux/Mac
```

3. Ensure write permissions:
```bash
chmod -R 755 chroma_db/
```

---

### Issue: Model download fails or is very slow

**Symptoms:**
```
Downloading model... (stuck)
```

**Solutions:**
1. Check internet connection

2. Use mirror or manual download:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models')
```

3. Download manually from HuggingFace and load locally

4. Use alternative model:
```python
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
```

---

### Issue: Out of memory during indexing

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**
1. Process in batches:
```python
batch_size = 50
for i in range(0, len(assessments), batch_size):
    batch = assessments[i:i+batch_size]
    # Process batch
```

2. Use smaller embedding model:
```python
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dim
# Instead of:
# model = SentenceTransformer('all-mpnet-base-v2')  # 768 dim
```

3. Increase system memory or use cloud instance

---

## API Issues

### Issue: API won't start

**Symptoms:**
```
ERROR: Address already in use
```

**Solutions:**
1. Kill process on port 8000:
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

2. Use different port:
```bash
uvicorn main:app --port 8080
```

---

### Issue: API returns 503 "Engine not initialized"

**Symptoms:**
```json
{"detail": "Engine not initialized. Build index first."}
```

**Solutions:**
1. Build index:
```bash
python embeddings.py
```

2. Verify index exists:
```bash
ls -la chroma_db/
```

3. Check logs for loading errors

---

### Issue: CORS errors in frontend

**Symptoms:**
```
Access to fetch at 'http://localhost:8000/recommend' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solutions:**
1. Update CORS in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Restart API server after changes

---

### Issue: API timeout on first request

**Symptoms:**
- First request takes 30+ seconds
- Subsequent requests are fast

**Cause:** Model loading on first request

**Solutions:**
1. Add warmup in startup event:
```python
@app.on_event("startup")
async def startup_event():
    # Warmup
    if engine:
        engine.recommend("test query", top_k=1)
```

2. Pre-load models before starting server

---

## Evaluation Issues

### Issue: Low Recall@K scores

**Symptoms:**
```
Mean Recall@10: 0.23
```

**Solutions:**

1. **Improve embeddings:**
```python
# Use better model
model = SentenceTransformer('all-mpnet-base-v2')
```

2. **Increase retrieval size:**
```python
candidates = em.search(query, k=30)  # Instead of k=20
```

3. **Improve query enhancement:**
```python
def enhance_query(query):
    # Extract key terms
    # Expand with synonyms
    # Add context
    return enhanced_query
```

4. **Tune K/P weights:**
```python
# Experiment with different weight strategies
weights = {'K': 0.6, 'P': 0.4}  # Try different ratios
```

5. **Check labeled data quality:**
- Ensure ground truth URLs are correct
- Verify URLs match scraped data
- Add more relevant assessments per query

---

### Issue: Labeled queries file not found

**Symptoms:**
```
FileNotFoundError: data/labeled_queries.json
```

**Solutions:**
1. Create from sample:
```bash
cp data/sample_labeled_queries.json data/labeled_queries.json
```

2. Add your actual labeled queries

3. Verify format:
```json
{
  "train_queries": [...],
  "test_queries": [...]
}
```

---

## Frontend Issues

### Issue: Frontend can't connect to API

**Symptoms:**
```
Failed to fetch
Network error
```

**Solutions:**
1. Verify API is running:
```bash
curl http://localhost:8000/health
```

2. Check .env file:
```bash
cat .env
# Should contain:
# VITE_API_URL=http://localhost:8000
```

3. Restart frontend after .env changes:
```bash
npm run dev
```

4. Check browser console for errors

---

### Issue: Build fails

**Symptoms:**
```
npm run build
ERROR: ...
```

**Solutions:**
1. Check for TypeScript errors (if using TS)

2. Verify all imports are correct

3. Clear cache and rebuild:
```bash
rm -rf node_modules dist
npm install
npm run build
```

4. Check for environment variable issues

---

## Deployment Issues

### Issue: Render deployment fails

**Symptoms:**
```
Build failed
Deploy failed
```

**Solutions:**

1. **Check build logs** in Render dashboard

2. **Verify requirements.txt:**
```bash
pip freeze > requirements.txt
```

3. **Add Python version** (create `runtime.txt`):
```
python-3.11.0
```

4. **Check start command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

5. **Commit data files:**
```bash
git add data/ chroma_db/
git commit -m "Add data and index"
git push
```

---

### Issue: Vercel deployment fails

**Symptoms:**
```
Build failed
```

**Solutions:**

1. **Check build logs** in Vercel dashboard

2. **Verify build command:**
```
npm run build
```

3. **Verify output directory:**
```
dist
```

4. **Check environment variables:**
- Add `VITE_API_URL` in Vercel dashboard
- Value: `https://your-api.render.com`

5. **Ensure package.json is correct:**
```json
{
  "scripts": {
    "build": "vite build"
  }
}
```

---

### Issue: Deployed API returns 500 errors

**Symptoms:**
- Works locally
- Fails in production

**Solutions:**

1. **Check logs** in Render dashboard

2. **Verify data files are deployed:**
```bash
# In Render shell:
ls -la data/
ls -la chroma_db/
```

3. **Use persistent disk** in Render:
- Add disk in Render dashboard
- Mount at `/app/chroma_db`

4. **Check environment variables**

5. **Verify model downloads work:**
- May need to pre-download models
- Or use persistent storage

---

## Performance Issues

### Issue: Slow query response (>5 seconds)

**Symptoms:**
- API takes too long to respond
- Frontend times out

**Solutions:**

1. **Profile the code:**
```python
import time
start = time.time()
# ... code ...
print(f"Took {time.time() - start:.2f}s")
```

2. **Reduce retrieval size:**
```python
candidates = em.search(query, k=10)  # Instead of k=20
```

3. **Skip re-ranking for fast mode:**
```python
if fast_mode:
    return candidates[:10]
else:
    return em.rerank(query, candidates)[:10]
```

4. **Add caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_recommendations(query: str):
    # ...
```

5. **Use async processing:**
```python
@app.post("/recommend")
async def recommend(request: RecommendRequest):
    # Use async/await
```

---

### Issue: High memory usage

**Symptoms:**
- Server crashes
- Out of memory errors

**Solutions:**

1. **Use smaller model:**
```python
model = SentenceTransformer('all-MiniLM-L6-v2')  # 80MB
# Instead of:
# model = SentenceTransformer('all-mpnet-base-v2')  # 420MB
```

2. **Limit batch size:**
```python
batch_size = 32  # Instead of 128
```

3. **Clear cache periodically:**
```python
import gc
gc.collect()
```

4. **Upgrade server resources**

---

## Data Quality Issues

### Issue: Recommendations not relevant

**Symptoms:**
- Results don't match query
- Wrong test types returned

**Solutions:**

1. **Improve text enrichment:**
```python
def create_enriched_text(assessment):
    # Add more context
    # Include more fields
    # Better formatting
```

2. **Check K/P classification:**
```python
# Verify test_type is correct
for a in assessments:
    print(f"{a['name']}: {a['test_type']}")
```

3. **Improve query analysis:**
```python
# Add more keywords
# Better weight calculation
# Context-aware analysis
```

4. **Use better embeddings:**
```python
# Try different models
# Or use OpenAI embeddings
```

---

## Testing Issues

### Issue: Tests fail

**Symptoms:**
```
python test_system.py
✗ FAIL: ...
```

**Solutions:**

1. **Read error messages carefully**

2. **Run tests individually:**
```python
# In test_system.py, comment out other tests
# Run one at a time
```

3. **Check dependencies:**
```bash
pip list
```

4. **Verify data exists:**
```bash
ls -la data/
ls -la chroma_db/
```

5. **Reset and rebuild:**
```bash
rm -rf chroma_db/
python embeddings.py
python test_system.py
```

---

## Getting Help

If you're still stuck:

1. **Check logs:**
   - Backend: Terminal output
   - Frontend: Browser console (F12)
   - Deployment: Platform dashboards

2. **Verify setup:**
```bash
python verify_setup.py
```

3. **Run system tests:**
```bash
python test_system.py
```

4. **Check documentation:**
   - README.md
   - QUICKSTART.md
   - ARCHITECTURE.md

5. **Search for error messages:**
   - Google the exact error
   - Check GitHub issues
   - Stack Overflow

6. **Start fresh:**
```bash
# Clean everything
rm -rf chroma_db/ data/*.json
rm -rf frontend/node_modules frontend/dist

# Rebuild
python quick_test.py
```

---

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| `ModuleNotFoundError` | Missing package | `pip install <package>` |
| `FileNotFoundError` | Missing data file | Run scraper or use sample data |
| `ConnectionError` | API not running | Start API with `uvicorn main:app` |
| `CORS error` | CORS not configured | Update `allow_origins` in main.py |
| `503 Service Unavailable` | Index not built | Run `python embeddings.py` |
| `MemoryError` | Out of memory | Use smaller model or batch size |
| `Address already in use` | Port occupied | Kill process or use different port |
| `Invalid collection` | ChromaDB issue | Delete and rebuild chroma_db/ |

---

## Prevention Tips

1. **Use virtual environment** for Python
2. **Commit frequently** to git
3. **Test locally** before deploying
4. **Keep backups** of data files
5. **Document changes** as you make them
6. **Run tests** after major changes
7. **Monitor logs** during development
8. **Use version control** for all code
