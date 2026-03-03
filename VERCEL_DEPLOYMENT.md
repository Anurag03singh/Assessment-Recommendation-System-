# Deploy Everything on Vercel

Yes! You can deploy both frontend and backend on Vercel. Here's how:

## Option 1: Separate Deployments (Recommended)

### Step 1: Deploy Backend API

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure:
   - **Project Name**: `shl-api`
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r ../requirements.txt && python embeddings.py`
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r ../requirements.txt`

4. Add `vercel.json` in backend directory:

Create `backend/vercel.json`:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

5. Deploy!
6. Copy your API URL: `https://shl-api.vercel.app`

### Step 2: Deploy Frontend

1. Go to https://vercel.com/new (again)
2. Import same GitHub repository
3. Configure:
   - **Project Name**: `shl-frontend`
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_URL` = `https://shl-api.vercel.app`

4. Deploy!
5. Copy your frontend URL: `https://shl-frontend.vercel.app`

---

## Option 2: Monorepo (Single Deployment)

Deploy as a monorepo with both frontend and backend:

### Create vercel.json in root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "frontend/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/dist/$1"
    }
  ]
}
```

### Update frontend to use /api prefix:

In `frontend/.env`:
```
VITE_API_URL=/api
```

### Deploy:
1. Go to https://vercel.com/new
2. Import repository
3. Deploy!

---

## Quick Setup (Easiest)

### 1. Create Backend Vercel Config

Create `backend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

### 2. Create requirements.txt in backend

Create `backend/requirements.txt` (copy from root):
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
sentence-transformers>=2.2.2
torch>=2.0.0
transformers>=4.35.0
chromadb>=0.4.18
numpy>=1.24.0
pandas>=2.1.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dotenv>=1.0.0
```

### 3. Deploy Backend
```bash
cd backend
vercel --prod
```

### 4. Deploy Frontend
```bash
cd frontend
vercel --prod --env VITE_API_URL=https://your-backend-url.vercel.app
```

---

## Advantages of Vercel

✅ **Free tier is generous**
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- Global CDN

✅ **Automatic deployments**
- Push to GitHub → Auto deploy
- Preview deployments for PRs

✅ **Fast**
- Edge network
- Instant cache invalidation

✅ **Easy**
- One command deployment
- No configuration needed

---

## Testing

### Backend
```bash
curl https://your-backend.vercel.app/health
```

### Frontend
Open `https://your-frontend.vercel.app` in browser

---

## Environment Variables

### Backend (if needed)
```
EMBEDDING_MODEL=all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
```

### Frontend (required)
```
VITE_API_URL=https://your-backend.vercel.app
```

---

## Troubleshooting

### Backend Build Fails
- Check Python version in vercel.json
- Verify requirements.txt is in backend directory
- Check logs in Vercel dashboard

### Frontend Can't Connect to Backend
- Verify VITE_API_URL is set correctly
- Check CORS is enabled in backend
- Test backend URL directly

### ChromaDB Issues
- Vercel has limited file system
- Embeddings need to be rebuilt on each deploy
- Consider using Vercel's persistent storage for production

---

## Cost

**Free Tier:**
- Perfect for this project
- 100GB bandwidth
- Unlimited deployments

**Pro Tier ($20/month):**
- Only if you need more bandwidth
- Not required for submission

---

## Quick Commands

### Deploy Backend
```bash
cd backend
vercel --prod
```

### Deploy Frontend
```bash
cd frontend
vercel --prod
```

### Update Environment Variable
```bash
vercel env add VITE_API_URL production
```

---

## For Submission

After deploying both:

1. **Backend URL**: `https://shl-api-xxx.vercel.app`
2. **Frontend URL**: `https://shl-frontend-xxx.vercel.app`
3. **GitHub**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

---

**Vercel is actually easier than Render for this project! 🚀**
