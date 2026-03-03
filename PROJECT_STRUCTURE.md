# Project Structure

```
shl-assessment-recommender/
│
├── backend/                          # Backend API and ML components
│   ├── data/                         # Data files
│   │   ├── shl_catalog.json         # Assessment catalog (54 assessments)
│   │   ├── labeled_queries.json     # Training and test queries
│   │   ├── submission.csv           # Generated predictions
│   │   └── Gen_AI_Dataset.xlsx      # Original dataset
│   │
│   ├── chroma_db/                    # Vector database (generated)
│   │
│   ├── main.py                       # FastAPI application
│   ├── embeddings.py                 # Vector store and embeddings
│   ├── recommender.py                # Recommendation engine
│   ├── evaluate.py                   # Evaluation metrics
│   ├── export_csv.py                 # CSV export utility
│   ├── scraper.py                    # Web scraping utilities
│   ├── create_catalog_from_urls.py   # Catalog builder
│   ├── build_catalog_from_dataset.py # Dataset processor
│   └── process_provided_dataset.py   # Excel data processor
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── App.jsx                  # Main application component
│   │   └── index.css                # Styles
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Vite configuration
│
├── README.md                         # Project overview
├── TECHNICAL_APPROACH.md             # Technical documentation
├── DEPLOYMENT_GUIDE.md               # Deployment instructions
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── setup.sh                          # Unix setup script
└── setup.bat                         # Windows setup script
```

## Key Components

### Backend

**main.py**
- FastAPI application
- API endpoints (/health, /recommend)
- Request/response handling

**embeddings.py**
- Sentence-BERT embedding generation
- ChromaDB vector store management
- Similarity search

**recommender.py**
- Query analysis
- Cross-encoder re-ranking
- K/P balancing logic

**evaluate.py**
- Mean Recall@10 calculation
- Performance metrics

**export_csv.py**
- Generates submission CSV
- Formats predictions

### Frontend

**App.jsx**
- React application
- Query input interface
- Results display
- API integration

### Data

**shl_catalog.json**
- 54 SHL assessments
- Structured metadata
- Test type categorization

**labeled_queries.json**
- 10 training queries
- 9 test queries
- Relevant assessment labels

**submission.csv**
- 90 rows (9 queries × 10 recommendations)
- Ready for submission

## Data Flow

```
User Query
    ↓
Frontend (React)
    ↓
Backend API (FastAPI)
    ↓
Embedding Generation (sentence-BERT)
    ↓
Vector Search (ChromaDB)
    ↓
Re-ranking (Cross-encoder)
    ↓
Balancing (K/P filter)
    ↓
Top 10 Recommendations
    ↓
Response to Frontend
```

## Technology Stack

- **Backend**: Python 3.10+, FastAPI
- **ML/NLP**: sentence-transformers, ChromaDB
- **Frontend**: React, Vite
- **Data**: pandas, BeautifulSoup4
