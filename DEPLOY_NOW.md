# 🚀 Deploy Now - Quick Reference

## Render Deployment (Backend)

### Configuration
```
Name: shl-recommender-api
Environment: Python 3
Branch: main

Build Command:
pip install -r requirements.txt && python backend/embeddings.py

Start Command:
uvicorn app:app --host 0.0.0.0 --port $PORT

Instance: Free
```

### Steps
1. Go to https://render.com/dashboard
2. New + → Web Service
3. Connect GitHub: `Assessment-Recommendation-System-`
4. Paste commands above
5. Create Web Service
6. Wait 5-10 minutes
7. Copy your URL: `https://your-app.onrender.com`

---

## Vercel Deployment (Frontend)

### Configuration
```
Framework: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist

Environment Variable:
VITE_API_URL=https://your-backend-url.onrender.com
```

### Steps
1. Go to https://vercel.com/new
2. Import GitHub: `Assessment-Recommendation-System-`
3. Configure as above
4. Deploy
5. Copy your URL: `https://your-app.vercel.app`

---

## Testing After Deployment

### Backend
```bash
# Health check
curl https://your-backend.onrender.com/health

# Test recommendation
curl -X POST https://your-backend.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query":"Java developer"}'
```

### Frontend
Open `https://your-frontend.vercel.app` in browser

---

## Submission Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Both URLs tested and working
- [ ] GitHub repository: https://github.com/Anurag03singh/Assessment-Recommendation-System-
- [ ] Technical document: TECHNICAL_APPROACH.md
- [ ] CSV file: backend/data/submission.csv

---

## URLs for Submission

**GitHub**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

**Backend API**: `https://________________.onrender.com`

**Frontend**: `https://________________.vercel.app`

---

## If Build Fails

1. Check logs in Render dashboard
2. Verify latest commit is deployed
3. Try manual deploy
4. Check RENDER_DEPLOYMENT.md for troubleshooting

---

**Everything is ready - just deploy! 🎉**
