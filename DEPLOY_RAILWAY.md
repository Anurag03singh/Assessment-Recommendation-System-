# Deploy to Railway (Best Free Option!)

Railway has a generous free tier perfect for ML apps:
- **512MB RAM** but more forgiving than Render
- **$5 free credit/month** (enough for ~500 hours)
- **Better cold start handling**
- **Persistent storage** for your embeddings

## Quick Deploy (3 minutes)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy from GitHub
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `Assessment-Recommendation-System-` repo
4. Railway will auto-detect it's a Python app

### Step 3: Configure
1. **Root Directory:** Set to `backend`
2. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables:**
   - `USE_LITE_MODE=true`
   - `SKIP_RERANKING=true`
   - `PORT=8000`

### Step 4: Deploy
Click "Deploy" and wait ~3 minutes

## Get Your URL

After deployment:
1. Go to "Settings" tab
2. Click "Generate Domain"
3. Your API will be at: `https://your-app.railway.app`

## Test Your API

```bash
# Replace with your Railway URL
export API_URL="https://your-app.railway.app"

# Health check
curl $API_URL/health

# Test recommendation
curl -X POST $API_URL/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python developer with SQL skills",
    "top_k": 5
  }'
```

## Why Railway?

✅ **Works with ML models** - Better memory handling
✅ **Free tier** - $5 credit/month (plenty for testing)
✅ **Auto-deploy** - Connects to GitHub
✅ **Persistent storage** - Your embeddings stay loaded
✅ **No sleep** - Unlike Render free tier

## Alternative: Fly.io

If Railway doesn't work, try Fly.io:

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
cd backend
flyctl launch

# Follow prompts, it will auto-configure
```

Fly.io free tier:
- 3 shared-cpu VMs
- 256MB RAM each
- Good for APIs

## Cost Comparison

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| Railway | $5 credit/month | ML apps (recommended) |
| Fly.io | 3x256MB VMs | Multiple small services |
| Render | 512MB (strict) | Simple apps only |
| Vercel | 1GB but size limits | Lightweight APIs |

## Recommendation

**Use Railway** - It's the sweet spot for your ML-based API with pre-built embeddings.
