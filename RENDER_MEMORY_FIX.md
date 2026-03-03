# Render Memory Optimization Guide

Your deployment is failing due to out-of-memory (OOM) errors on Render's free tier (512MB limit).

## Solution Options

### Option 1: Upgrade to Paid Plan (Easiest)
Upgrade to Render's **Starter plan ($7/month)** which provides 2GB RAM.
- Go to your service settings on Render
- Change instance type to "Starter"
- Redeploy

### Option 2: Use Pre-built Embeddings (Free Tier Compatible)

Build embeddings locally and deploy the database:

1. **Build embeddings locally:**
```bash
cd backend
python embeddings.py
```

This creates a `chroma_db` folder with pre-computed embeddings.

2. **Add chroma_db to your repo:**
```bash
git add chroma_db/
git commit -m "Add pre-built embeddings"
git push
```

3. **Set environment variables on Render:**
- `USE_LITE_MODE=true`
- `SKIP_RERANKING=true`

4. **Redeploy** - The app will load pre-built embeddings instead of building them.

### Option 3: Deploy to Alternative Platform

**Vercel (Recommended for Free Tier):**
- Supports serverless functions
- Better memory limits
- See `VERCEL_DEPLOYMENT.md`

**Railway:**
- Free tier: 512MB RAM + 500 hours/month
- Similar to Render but sometimes more forgiving

**Fly.io:**
- Free tier: 256MB RAM (3 instances)
- Can scale better

## Memory Usage Breakdown

Current stack memory usage:
- PyTorch: ~200MB
- Sentence Transformers models: ~180MB
- ChromaDB: ~50MB
- FastAPI + dependencies: ~50MB
- **Total: ~480MB** (very close to 512MB limit)

With pre-built embeddings:
- No model loading on startup
- Embeddings loaded from disk as needed
- **Peak usage: ~300MB** (fits in free tier)

## Quick Fix Commands

```bash
# Build embeddings locally
cd backend
python embeddings.py

# Add to git
git add chroma_db/
git commit -m "Add pre-built embeddings"
git push

# On Render dashboard, add environment variables:
# USE_LITE_MODE=true
# SKIP_RERANKING=true
```

## Verification

After deployment, test the API:
```bash
curl https://your-app.onrender.com/health
curl -X POST https://your-app.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Python developer", "top_k": 5}'
```
