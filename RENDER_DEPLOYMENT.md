# Render Deployment Guide

## Quick Setup

### Step 1: Create Web Service

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select repository: `Assessment-Recommendation-System-`

### Step 2: Configure Service

**Basic Settings:**
- **Name**: `shl-recommender-api` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python backend/embeddings.py
  ```
- **Start Command**: 
  ```
  uvicorn app:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** (for testing)

### Step 3: Deploy

1. Click **"Create Web Service"**
2. Wait for build (5-10 minutes)
3. Watch the logs for any errors

### Step 4: Get Your URL

Once deployed, your API will be available at:
```
https://shl-recommender-api.onrender.com
```

## Testing Your Deployment

### Test Health Endpoint
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test Recommendation Endpoint
```bash
curl -X POST https://your-app-name.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills"}'
```

## Common Issues & Solutions

### Issue 1: Build Fails - Torch Version
**Error**: `Could not find a version that satisfies the requirement torch==2.1.0`

**Solution**: Already fixed! The requirements.txt now uses `torch>=2.0.0` which is compatible with Python 3.14.

### Issue 2: Build Timeout
**Error**: Build takes too long

**Solution**: 
- Use Free tier (has longer timeout)
- Or split build: Install deps first, then build index separately

### Issue 3: Memory Issues During Build
**Error**: Out of memory during embeddings.py

**Solution**: The embeddings will be built during deployment. If it fails:
1. Comment out the embeddings build in build command
2. Deploy first
3. Build embeddings manually via Render shell

### Issue 4: ChromaDB Persistence
**Note**: Free tier doesn't persist files between deploys

**Solution**: 
- Embeddings are rebuilt on each deploy (included in build command)
- For production, use paid tier with persistent disk

## Alternative Build Commands

### Option 1: Standard (Recommended)
```bash
pip install -r requirements.txt && python backend/embeddings.py
```

### Option 2: If embeddings.py fails
```bash
pip install -r requirements.txt
```
Then build embeddings after first deploy via shell.

### Option 3: With caching
```bash
pip install --cache-dir /tmp/pip-cache -r requirements.txt && python backend/embeddings.py
```

## Environment Variables (Optional)

You can add these in Render dashboard:

```
EMBEDDING_MODEL=all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
PYTHON_VERSION=3.11.0
```

## Monitoring

### View Logs
1. Go to your service dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs

### Check Status
- Green dot = Running
- Yellow dot = Building
- Red dot = Failed

## Updating Your Deployment

### Automatic Updates
Render automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update code"
git push origin main
```

### Manual Deploy
1. Go to service dashboard
2. Click **"Manual Deploy"**
3. Select **"Deploy latest commit"**

## Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- First request after spin-down takes ~30 seconds
- 750 hours/month free
- No persistent disk (files reset on deploy)

## Upgrading to Paid

For production use:
- **Starter**: $7/month - Always on, persistent disk
- **Standard**: $25/month - More resources

## Support

If deployment fails:
1. Check logs in Render dashboard
2. Verify requirements.txt is correct
3. Test locally first: `pip install -r requirements.txt`
4. Check GitHub repo is up to date

## Success Checklist

- [ ] Service created on Render
- [ ] Build completed successfully
- [ ] Service is running (green status)
- [ ] Health endpoint returns 200
- [ ] Recommend endpoint works
- [ ] URL noted for submission

---

**Your API URL**: `https://your-app-name.onrender.com`

Copy this URL for:
1. Frontend environment variable
2. Submission form
3. Testing
