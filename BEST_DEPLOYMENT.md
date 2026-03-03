# Best Deployment Strategy

## The Problem with Vercel Backend

❌ **Vercel Serverless Limitation**: 500 MB max  
❌ **Our Dependencies**: 7.3 GB (PyTorch, transformers, etc.)  
❌ **Result**: Too large for Vercel serverless functions

## ✅ Best Solution: Render + Vercel

### Backend → Render (Free, No Size Limit)
### Frontend → Vercel (Fast, Free CDN)

---

## Deploy Backend on Render (10 minutes)

### Step 1: Go to Render
https://render.com/dashboard

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub: `Assessment-Recommendation-System-`
3. Configure:

```
Name: shl-api
Environment: Python 3
Branch: main

Build Command:
pip install -r requirements.txt && python backend/embeddings.py

Start Command:
uvicorn app:app --host 0.0.0.0 --port $PORT

Instance: Free
```

4. Click **"Create Web Service"**
5. Wait 5-10 minutes
6. Copy URL: `https://shl-api.onrender.com`

---

## Deploy Frontend on Vercel (3 minutes)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
vercel login
```

### Step 2: Set Backend URL
Create `frontend/.env.production`:
```
VITE_API_URL=https://shl-api.onrender.com
```
(Use your actual Render URL)

### Step 3: Deploy
```bash
cd frontend
vercel --prod
```

Copy URL: `https://shl-frontend.vercel.app`

---

## Why This Combination?

### Render for Backend ✅
- **No size limits** - Perfect for ML models
- **Always-on option** - Can upgrade if needed
- **Free tier** - 750 hours/month
- **Persistent storage** - For ChromaDB

### Vercel for Frontend ✅
- **Lightning fast** - Global CDN
- **Free** - Unlimited bandwidth
- **Auto-deploy** - On git push
- **Perfect for React** - Built for it

---

## Alternative: Railway (Backend)

If Render doesn't work, try Railway:

### Railway Deployment
1. Go to https://railway.app
2. **"New Project"** → **"Deploy from GitHub"**
3. Select repository
4. Railway auto-detects Python
5. Add start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Deploy!

---

## Testing

### Backend (Render)
```bash
curl https://shl-api.onrender.com/health
```

### Frontend (Vercel)
```
https://shl-frontend.vercel.app
```

---

## Cost

**Total: $0/month**
- Render Free: 750 hours
- Vercel Free: Unlimited

---

## For Submission

**GitHub**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

**Backend API**: `https://shl-api.onrender.com`

**Frontend**: `https://shl-frontend.vercel.app`

**Technical Doc**: TECHNICAL_APPROACH.md

**CSV File**: backend/data/submission.csv

---

## Quick Commands

### Backend (Render)
Use web interface - no CLI needed

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

---

## Summary

✅ **Backend**: Render (handles large ML dependencies)  
✅ **Frontend**: Vercel (fast, free, perfect for React)  
✅ **Total Cost**: $0  
✅ **Total Time**: ~15 minutes  

**This is the best approach for ML applications! 🚀**
