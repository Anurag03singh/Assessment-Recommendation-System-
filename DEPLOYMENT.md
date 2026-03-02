# Deployment Guide

## Backend (Render / Railway)

1. Create new Web Service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables if needed
6. Deploy

## Frontend (Vercel)

1. Import project from GitHub
2. Framework: Vite
3. Build command: `npm run build`
4. Output directory: `dist`
5. Add environment variable: `VITE_API_URL=<your-backend-url>`
6. Deploy

## Pre-deployment Checklist

- [ ] Run scraper: `python backend/scraper.py`
- [ ] Verify 377+ assessments scraped
- [ ] Build index: `python backend/embeddings.py`
- [ ] Test API locally: `uvicorn main:app --reload`
- [ ] Run evaluation: `python backend/evaluate.py`
- [ ] Export CSV: `python backend/export_csv.py`
- [ ] Test frontend locally: `npm run dev`
- [ ] Update CORS origins in main.py
- [ ] Commit chroma_db/ and data/ to repo (or use persistent storage)
