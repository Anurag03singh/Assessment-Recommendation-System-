# Deployment Guide

## Prerequisites

- GitHub account
- Render account (for backend) - https://render.com
- Vercel account (for frontend) - https://vercel.com

## Backend Deployment (Render)

### 1. Prepare Repository

Ensure your code is pushed to GitHub:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy on Render

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `shl-recommender-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && cd backend && python embeddings.py`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes)
7. Note your API URL: `https://shl-recommender-api.onrender.com`

### 3. Test Deployment

```bash
curl https://your-api-url.onrender.com/health
```

## Frontend Deployment (Vercel)

### 1. Update API URL

Create `frontend/.env`:
```
VITE_API_URL=https://your-api-url.onrender.com
```

### 2. Deploy to Vercel

**Using Vercel CLI:**
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

**Using Vercel Dashboard:**
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Environment Variables**: `VITE_API_URL=https://your-api-url.onrender.com`
5. Click "Deploy"
6. Note your frontend URL: `https://shl-recommender.vercel.app`

## Verification

### Test Backend
```bash
curl -X POST https://your-api-url/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer"}'
```

### Test Frontend
Open `https://your-frontend-url` in browser and test with a sample query.

## Troubleshooting

**Backend Issues:**
- Check logs in Render dashboard
- Verify build command completed successfully
- Ensure all dependencies are in requirements.txt

**Frontend Issues:**
- Verify VITE_API_URL is set correctly
- Check browser console for errors
- Ensure CORS is enabled in backend

## Environment Variables

### Backend (Optional)
```
EMBEDDING_MODEL=all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
```

### Frontend (Required)
```
VITE_API_URL=https://your-backend-url
```

## Continuous Deployment

Both Render and Vercel support automatic deployment:
- Push to GitHub → Automatic build and deploy
- Takes 2-5 minutes per deployment

## Alternative Platforms

### Backend
- Railway: https://railway.app
- Google Cloud Run
- Heroku

### Frontend
- Netlify: https://netlify.com
- GitHub Pages
- Cloudflare Pages

## Support

For deployment issues:
1. Check platform documentation
2. Review deployment logs
3. Verify environment variables
4. Test locally first
