# Documentation Index

Complete guide to all documentation files in this project.

## 🚀 Getting Started (Read These First)

1. **[README.md](README.md)** - Project overview and quick links
2. **[verify_setup.py](verify_setup.py)** - Verify all files are present
3. **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup guide
4. **[COMMANDS.md](COMMANDS.md)** - All commands you'll need

## 📚 Core Documentation

### Architecture & Design
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture with ASCII diagrams
  - High-level overview
  - Data flow diagrams
  - Component architecture
  - Deployment architecture
  - Scalability considerations

- **[TECHNICAL_DOCUMENT.md](TECHNICAL_DOCUMENT.md)** - 2-page technical document
  - Page 1: System design, data pipeline, embedding strategy
  - Page 2: Evaluation, optimization, results
  - **Use this for submission**

### Development Guides
- **[WORKFLOW.md](WORKFLOW.md)** - Complete development workflow
  - Phase-by-phase implementation
  - Day-by-day timeline
  - Validation steps
  - Troubleshooting per phase

- **[CHECKLIST.md](CHECKLIST.md)** - Implementation checklist
  - Setup tasks
  - Development tasks
  - Testing tasks
  - Deployment tasks
  - Time estimates

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview
  - What we built
  - Key features
  - Tech stack
  - How it works
  - Success criteria

### Operations
- **[COMMANDS.md](COMMANDS.md)** - Command reference
  - Setup commands
  - Backend commands
  - Frontend commands
  - API testing
  - Docker commands
  - Git commands
  - Deployment commands
  - Troubleshooting commands

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide
  - Backend deployment (Render)
  - Frontend deployment (Vercel)
  - Pre-deployment checklist
  - Post-deployment verification

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving
  - Setup issues
  - Scraping issues
  - API issues
  - Frontend issues
  - Deployment issues
  - Performance issues
  - Common error messages

## 🔧 Code Files

### Backend (Python)

#### Core Application
- **backend/main.py** - FastAPI application
  - `/health` - Health check endpoint
  - `/recommend` - Recommendation endpoint
  - `/stats` - Statistics endpoint
  - CORS configuration

- **backend/scraper.py** - Web scraper
  - SHLScraper class
  - Crawls SHL product catalog
  - Extracts 377+ assessments
  - K/P classification
  - Saves to JSON

- **backend/embeddings.py** - Embedding & vector store
  - EmbeddingManager class
  - Sentence Transformers integration
  - ChromaDB management
  - Vector search
  - Cross-encoder re-ranking

- **backend/recommender.py** - Recommendation engine
  - RecommendationEngine class
  - Query analysis
  - K/P weight calculation
  - Balanced filtering
  - Top-K selection

#### Utilities
- **backend/evaluate.py** - Evaluation framework
  - Recall@K calculation
  - Evaluator class
  - Ablation study support
  - Results export

- **backend/export_csv.py** - CSV export
  - Exports test results
  - Submission format
  - 9 queries × 10 recommendations

- **backend/test_system.py** - System tests
  - Data availability test
  - Embeddings test
  - Recommender test
  - API test
  - Evaluation test

- **backend/setup.py** - Setup wizard
  - Interactive setup
  - Dependency check
  - Directory creation
  - Scraper execution
  - Index building

- **backend/quick_test.py** - Quick test
  - Uses sample data
  - Fast verification
  - No scraping needed

#### Configuration
- **backend/requirements.txt** - Python dependencies
- **backend/Dockerfile** - Docker configuration
- **backend/.env** - Environment variables (create this)

#### Data Files
- **backend/data/sample_catalog.json** - Sample assessments (10 items)
- **backend/data/sample_labeled_queries.json** - Sample queries
- **backend/data/shl_catalog.json** - Full catalog (created by scraper)
- **backend/data/labeled_queries.json** - Your labeled queries (create this)
- **backend/data/evaluation_results.json** - Evaluation output
- **backend/data/submission.csv** - CSV for submission

### Frontend (React)

#### Application
- **frontend/src/App.jsx** - Main React component
  - Query input form
  - JD URL input
  - Results display
  - K/P balance visualization

- **frontend/src/main.jsx** - React entry point
- **frontend/src/index.css** - Tailwind CSS imports

#### Configuration
- **frontend/package.json** - NPM dependencies
- **frontend/vite.config.js** - Vite configuration
- **frontend/tailwind.config.js** - Tailwind configuration
- **frontend/postcss.config.js** - PostCSS configuration
- **frontend/index.html** - HTML template
- **frontend/.env** - Environment variables (create this)
- **frontend/.env.example** - Environment template

### Configuration Files
- **.gitignore** - Git ignore rules
- **verify_setup.py** - Setup verification script

## 📖 Reading Order by Use Case

### First Time Setup
1. README.md - Overview
2. verify_setup.py - Check files
3. QUICKSTART.md - Setup instructions
4. COMMANDS.md - Command reference

### Understanding the System
1. PROJECT_SUMMARY.md - What we built
2. ARCHITECTURE.md - How it works
3. TECHNICAL_DOCUMENT.md - Detailed design

### Development
1. WORKFLOW.md - Step-by-step process
2. CHECKLIST.md - Track progress
3. COMMANDS.md - Commands to run
4. TROUBLESHOOTING.md - When stuck

### Deployment
1. DEPLOYMENT.md - Deployment steps
2. CHECKLIST.md - Pre-deployment checks
3. TROUBLESHOOTING.md - Deployment issues

### Submission
1. TECHNICAL_DOCUMENT.md - Submit this
2. backend/data/submission.csv - Submit this
3. Deployed URLs - Include in submission

## 🎯 Quick Reference by Task

### "I want to set up the project"
→ QUICKSTART.md

### "I want to understand the architecture"
→ ARCHITECTURE.md

### "I want to see all available commands"
→ COMMANDS.md

### "I'm stuck with an error"
→ TROUBLESHOOTING.md

### "I want to deploy"
→ DEPLOYMENT.md

### "I want to track my progress"
→ CHECKLIST.md

### "I want to understand the workflow"
→ WORKFLOW.md

### "I need the submission document"
→ TECHNICAL_DOCUMENT.md

### "I want a complete overview"
→ PROJECT_SUMMARY.md

## 📊 File Statistics

### Documentation Files: 11
- README.md
- QUICKSTART.md
- TECHNICAL_DOCUMENT.md
- ARCHITECTURE.md
- WORKFLOW.md
- CHECKLIST.md
- PROJECT_SUMMARY.md
- DEPLOYMENT.md
- COMMANDS.md
- TROUBLESHOOTING.md
- INDEX.md (this file)

### Backend Files: 10
- main.py
- scraper.py
- embeddings.py
- recommender.py
- evaluate.py
- export_csv.py
- test_system.py
- setup.py
- quick_test.py
- requirements.txt

### Frontend Files: 7
- App.jsx
- main.jsx
- index.css
- index.html
- package.json
- vite.config.js
- tailwind.config.js

### Configuration Files: 4
- .gitignore
- Dockerfile
- postcss.config.js
- .env.example

### Data Files: 2 (samples)
- sample_catalog.json
- sample_labeled_queries.json

### Total Files: 34

## 🔍 Search Guide

### Looking for...

**Setup instructions?**
- QUICKSTART.md
- verify_setup.py

**Architecture diagrams?**
- ARCHITECTURE.md

**Command to run scraper?**
- COMMANDS.md → "Data Collection"

**How to deploy?**
- DEPLOYMENT.md

**Error solutions?**
- TROUBLESHOOTING.md

**Implementation timeline?**
- WORKFLOW.md
- CHECKLIST.md

**Submission requirements?**
- TECHNICAL_DOCUMENT.md
- PROJECT_SUMMARY.md → "Deliverables"

**API endpoints?**
- ARCHITECTURE.md → "Component Architecture"
- backend/main.py

**Evaluation metrics?**
- TECHNICAL_DOCUMENT.md → "Page 2"
- backend/evaluate.py

**Sample data?**
- backend/data/sample_catalog.json
- backend/data/sample_labeled_queries.json

## 💡 Tips

1. **Start with README.md** for overview
2. **Run verify_setup.py** to check files
3. **Follow QUICKSTART.md** for setup
4. **Use COMMANDS.md** as reference
5. **Check TROUBLESHOOTING.md** when stuck
6. **Track progress with CHECKLIST.md**
7. **Submit TECHNICAL_DOCUMENT.md**

## 🆘 Need Help?

1. Check TROUBLESHOOTING.md
2. Review relevant documentation
3. Run test_system.py
4. Check logs and error messages
5. Verify setup with verify_setup.py

## 📝 Notes

- All documentation is in Markdown format
- Code files have inline comments
- Sample data provided for testing
- Complete system ready to deploy
- Comprehensive testing included

---

**Last Updated:** Project creation
**Version:** 1.0
**Status:** Complete and ready for use
