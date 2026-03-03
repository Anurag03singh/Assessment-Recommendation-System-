# Fix Render Memory Issue

## Problem
Render free tier: 512MB RAM  
Building embeddings: Requires ~1GB RAM  
Result: Out of memory error

## Solution: Skip Embedding Build

### Option 1: Use Paid Tier (Recommended for Production)
- Upgrade to Starter ($7/month)
- 512MB → 2GB RAM
- Embeddings will build successfully

### Option 2: Modify Build Command (Free Tier Workaround)

**Change build command to:**
```
pip install -r requirements.txt
```

**Remove:** `&& python backend/embeddings.py`

**What happens:**
- Dependencies install successfully
- Embeddings build on first API request (lazy loading)
- First request takes ~30 seconds
- Subsequent requests are fast

### Option 3: Use Railway (Better Free Tier)

Railway offers more generous free tier:
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Railway auto-detects Python
5. Add start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Deploy!

**Railway Free Tier:**
- $5 free credit/month
- More memory than Render
- Should handle embedding build

---

## Quick Fix for Render

### Update Your Service:

1. Go to Render dashboard
2. Find your service
3. Click "Settings"
4. Update **Build Command** to:
   ```
   pip install -r requirements.txt
   ```
5. Save changes
6. Manual Deploy → Deploy latest commit

### Update app.py to handle lazy loading:

The embeddings will be built on first request automatically.

---

## Alternative: Deploy to Railway

**Step 1:** Go to https://railway.app

**Step 2:** New Project → Deploy from GitHub repo

**Step 3:** Configure:
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Build Command:** `pip install -r requirements.txt && python backend/embeddings.py`

**Step 4:** Deploy!

Railway has better memory limits and should work.

---

## Recommendation

**For Submission:**
1. Use Railway (free, more memory)
2. Or use Render without embedding build
3. Or upgrade Render to Starter ($7)

**Railway is the easiest solution for free deployment with ML models.**
