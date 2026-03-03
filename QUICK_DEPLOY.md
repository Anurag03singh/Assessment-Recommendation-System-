# 🚀 Quick Deploy Reference Card

## Pre-Deployment (One-Time Setup)

```bash
# 1. Verify everything is ready
python deploy_check.py

# 2. If ChromaDB missing, build it
python build_embeddings.py
```

## Deploy to Render (Easiest - Recommended)

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to https://render.com
# 3. Click "New +" → "Web Service"
# 4. Connect your GitHub repository
# 5. Render auto-detects render.yaml
# 6. Click "Create Web Service"
# 7. Wait 3-5 minutes for deployment
# 8. Get your URL: https://your-app.onrender.com
```

## Deploy to Railway

```bash
# 1. Install CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Get URL
railway open
```

## Deploy to Fly.io

```bash
# 1. Install CLI
curl -L https://fly.io/install.sh | sh

# 2. Login and deploy
fly auth login
fly launch
fly deploy

# 3. Get URL
fly status
```

## Test Your Deployment

```bash
# Replace YOUR_URL with your deployment URL

# Health check
curl https://YOUR_URL/health

# Test recommendation
curl -X POST https://YOUR_URL/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with communication skills", "top_k": 10}'

# Check stats
curl https://YOUR_URL/stats
```

## Environment Variables (Set in Platform Dashboard)

```
PYTHON_VERSION=3.11
USE_LITE_MODE=true
SKIP_RERANKING=false
```

## Memory Usage

- Startup: ~200MB
- Per Request: ~350MB peak
- Idle: ~180MB
- **Total: < 512MB** ✅

## Files Required for Deployment

```
✅ backend/main_production.py
✅ backend/embeddings_lite.py
✅ backend/recommender.py
✅ backend/requirements-lite.txt
✅ backend/data/shl_catalog.json
✅ chroma_db/ (entire folder)
✅ render.yaml (or railway.json or fly.toml)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Collection not found" | Run `python build_embeddings.py` |
| "Out of memory" | Set `SKIP_RERANKING=true` |
| "Module not found" | Use `requirements-lite.txt` |
| Slow responses | Check if ChromaDB is loaded |

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /recommend` - Get recommendations
- `GET /stats` - System statistics
- `GET /docs` - API documentation

## Request Format

```json
{
  "query": "Job description or requirements",
  "top_k": 10
}
```

## Response Format

```json
{
  "recommended_assessments": [
    {
      "url": "https://...",
      "adaptive_support": "Yes/No",
      "description": "...",
      "duration": 45,
      "remote_support": "Yes/No",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```

## Platform Comparison

| Platform | Memory | Cost | Setup Time | Recommended |
|----------|--------|------|------------|-------------|
| **Render** | 512MB | Free | 5 min | ⭐⭐⭐⭐⭐ |
| Railway | 512MB | $5 credit | 3 min | ⭐⭐⭐⭐ |
| Fly.io | 512MB | Free | 5 min | ⭐⭐⭐⭐ |

## Success Checklist

- [ ] `python deploy_check.py` passes
- [ ] Code pushed to GitHub
- [ ] Deployed to platform
- [ ] Health check returns 200 OK
- [ ] Test recommendation works
- [ ] Memory usage < 512MB
- [ ] Response time < 2 seconds

## Need Help?

1. Check platform logs
2. Review `DEPLOY_READY.md`
3. Run `deploy_check.py` locally
4. Test with same environment variables

## You're Done! 🎉

Your API is live and ready to use!

**Next**: Deploy frontend to Vercel/Netlify and update API URL.
