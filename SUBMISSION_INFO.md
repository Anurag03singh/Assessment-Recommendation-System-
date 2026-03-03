# Submission Information

## Project Details

**Project Name**: SHL Assessment Recommendation System  
**GitHub Repository**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

---

## Deliverables

### 1. ✅ GitHub Repository
**URL**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

**What's included:**
- Complete source code (backend + frontend)
- 54 real SHL assessments catalog
- Training and test data
- All documentation
- Setup scripts

### 2. ✅ Technical Document
**File**: `TECHNICAL_APPROACH.md`

**Contents:**
- Problem statement and solution architecture
- Data pipeline and recommendation engine details
- Performance optimization journey
- Technical decisions and rationale
- Evaluation methodology
- Results and examples

### 3. ✅ Submission CSV
**File**: `backend/data/submission.csv`

**Format**: Query, Assessment_url  
**Rows**: 90 (9 test queries × 10 recommendations)  
**Status**: Ready for submission

### 4. 🚀 API Endpoint (To Deploy)
**Local**: http://localhost:8000  
**Production**: (Deploy to Render/Railway)

**Endpoints:**
- `GET /health` - Health check
- `POST /recommend` - Get recommendations

### 5. 🌐 Frontend Application (To Deploy)
**Local**: http://localhost:3000  
**Production**: (Deploy to Vercel/Netlify)

---

## System Specifications

### Assessment Catalog
- **Total Assessments**: 54
- **Source**: Gen_AI_Dataset.xlsx (provided)
- **Categories**: Knowledge & Skills, Personality & Behaviour, Competencies, Ability & Aptitude

### Training Data
- **Train Queries**: 10 with labeled assessments
- **Test Queries**: 9 for submission
- **Source**: Gen_AI_Dataset.xlsx

### Technology Stack
- **Backend**: Python 3.10+, FastAPI
- **ML/NLP**: sentence-transformers (all-MiniLM-L6-v2), ChromaDB
- **Re-ranking**: Cross-encoder (ms-marco-MiniLM-L-6-v2)
- **Frontend**: React, Vite, TailwindCSS

---

## Key Features

1. **Semantic Search**
   - Uses sentence-BERT for understanding query intent
   - Goes beyond keyword matching

2. **Intelligent Balancing**
   - Analyzes queries for technical vs behavioral needs
   - Balances K and P type recommendations

3. **Re-ranking**
   - Cross-encoder improves top-10 relevance
   - More accurate than bi-encoder alone

4. **Real Data**
   - Built from provided Gen_AI_Dataset.xlsx
   - 54 real SHL assessment URLs

---

## Performance

### Example Results

**Query**: "Java developer with collaboration skills"
- Returns: Java assessments + teamwork/communication assessments
- Balance: 60% K, 40% P ✅

**Query**: "Sales representative for new graduates"
- Returns: Entry-level sales assessments
- Balance: 100% P (appropriate) ✅

**Query**: "Analyst with cognitive and personality tests"
- Returns: OPQ + Verify tests
- Balance: 20% K, 80% P ✅

---

## Deployment Instructions

### Backend (Render)
1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Build: `cd backend && pip install -r ../requirements.txt && python embeddings.py`
5. Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Go to https://vercel.com
2. Import GitHub repository
3. Root: `frontend`
4. Build: `npm run build`
5. Environment: `VITE_API_URL=<your-backend-url>`

---

## Files for Submission

### Required Files
1. **API URL**: (After deployment to Render)
2. **GitHub URL**: https://github.com/Anurag03singh/Assessment-Recommendation-System-
3. **Frontend URL**: (After deployment to Vercel)
4. **Technical Document**: TECHNICAL_APPROACH.md
5. **CSV File**: backend/data/submission.csv

### Supporting Documentation
- README.md - Project overview
- DEPLOYMENT_GUIDE.md - Deployment steps
- PROJECT_STRUCTURE.md - Code organization
- CONTRIBUTING.md - Contribution guidelines

---

## Local Testing

### Start Backend
```bash
cd backend
python main.py
```
Access: http://localhost:8000

### Start Frontend
```bash
cd frontend
npm run dev
```
Access: http://localhost:3000

### Test API
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills"}'
```

---

## Project Statistics

- **Lines of Code**: ~2,500
- **Python Files**: 7
- **Assessments**: 54
- **Test Queries**: 9
- **Recommendations per Query**: 10
- **Total CSV Rows**: 90

---

## Contact

**GitHub**: https://github.com/Anurag03singh  
**Repository**: https://github.com/Anurag03singh/Assessment-Recommendation-System-

---

**Status**: ✅ Complete and Ready for Submission  
**Last Updated**: March 2, 2026
