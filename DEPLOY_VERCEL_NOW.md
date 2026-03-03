# Deploy to Vercel (Recommended - Free Tier Works!)

Vercel has better memory limits for serverless functions and works great with ML models.

## Quick Deploy (2 minutes)

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel:** https://vercel.com/new
2. **Import your GitHub repo:** 
   - Click "Import Git Repository"
   - Select your `Assessment-Recommendation-System-` repo
3. **Configure:**
   - Framework Preset: `Other`
   - Root Directory: `backend`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. **Click "Deploy"**

That's it! Vercel will auto-deploy in ~2 minutes.

### Option 2: Deploy via CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy from backend folder
cd backend
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name? (press enter for default)
# - Directory? ./ (current directory)
# - Override settings? N

# Deploy to production
vercel --prod
```

## Your API Endpoint

After deployment, Vercel will give you a URL like:
```
https://your-project.vercel.app
```

Your API endpoints:
- Health: `https://your-project.vercel.app/health`
- Recommend: `https://your-project.vercel.app/recommend`

## Test Your API

```bash
# Replace with your Vercel URL
export API_URL="https://your-project.vercel.app"

# Health check
curl $API_URL/health

# Test recommendation
curl -X POST $API_URL/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Looking for Python developer with SQL skills",
    "top_k": 5
  }'
```

## Why Vercel Works Better

- **Memory:** 1GB for free tier (vs 512MB on Render)
- **Serverless:** Functions scale automatically
- **Cold starts:** ~3-5 seconds (acceptable for API)
- **No sleep:** Unlike Render free tier, no forced sleep
- **Easy updates:** Just `git push` and auto-deploys

## Troubleshooting

**If deployment fails:**

1. Check build logs in Vercel dashboard
2. Ensure `backend/chroma_db/` folder is in your repo
3. Try deploying from CLI for better error messages

**If API is slow on first request:**
- This is normal (cold start)
- Subsequent requests are fast (~200ms)
- Consider upgrading to Pro ($20/month) for faster cold starts

## Update Your Frontend

Once deployed, update your frontend to use the Vercel URL:

```javascript
// In frontend/src/App.jsx
const API_URL = "https://your-project.vercel.app";
```

## Auto-Deploy on Git Push

Vercel automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update API"
git push
```

Vercel detects changes and redeploys automatically!
