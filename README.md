# SHL Assessment Recommendation System

A machine learning-powered recommendation system that suggests relevant SHL assessments based on job descriptions and hiring requirements.

## Overview

This system uses semantic search and natural language processing to match job requirements with appropriate SHL assessments. It analyzes job descriptions and recommends a balanced mix of technical skills assessments and behavioral/personality tests.

## Features

- Semantic understanding of job descriptions using sentence transformers
- Intelligent balancing between Knowledge & Skills and Personality & Behaviour assessments
- Cross-encoder re-ranking for improved relevance
- REST API for easy integration
- Web interface for interactive testing

## Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **ML/NLP**: sentence-transformers, ChromaDB
- **Frontend**: React, Vite
- **Data Processing**: pandas, BeautifulSoup4

## Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 16+ (for frontend)

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Build the vector index
cd backend
python embeddings.py

# Start the API server
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The web interface will be available at `http://localhost:3000`

## API Usage

### Health Check
```bash
GET /health
```

### Get Recommendations
```bash
POST /recommend
Content-Type: application/json

{
  "query": "Looking for Java developers with strong communication skills"
}
```

Response:
```json
{
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/...",
      "adaptive_support": "No",
      "description": "Technical assessment...",
      "duration": 45,
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```

## Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── embeddings.py           # Vector store management
│   ├── recommender.py          # Recommendation engine
│   ├── evaluate.py             # Evaluation metrics
│   ├── export_csv.py           # CSV export utility
│   ├── scraper.py              # Data collection
│   └── data/
│       ├── shl_catalog.json    # Assessment catalog
│       └── labeled_queries.json # Training data
├── frontend/
│   └── src/
│       └── App.jsx             # React application
└── requirements.txt
```

## How It Works

1. **Data Collection**: Assessment catalog is built from SHL product URLs
2. **Embedding Generation**: Each assessment is converted to a semantic vector using sentence-BERT
3. **Query Processing**: User queries are analyzed to determine the balance of technical vs behavioral needs
4. **Retrieval**: Top candidates are retrieved using cosine similarity
5. **Re-ranking**: Cross-encoder model re-ranks candidates for better relevance
6. **Balancing**: Final recommendations are balanced between K and P type assessments

## Evaluation

The system is evaluated using Mean Recall@10:

```bash
cd backend
python evaluate.py
```

## Generating Submission Files

```bash
cd backend
python export_csv.py
```

This generates `data/submission.csv` with recommendations for all test queries.

## Configuration

Environment variables can be set in `.env`:

```
EMBEDDING_MODEL=all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
```

## Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions for Render, Vercel, and other platforms.

## License

This project was created as part of a technical assessment.

## Author

Developed as a solution for the SHL Assessment Recommendation challenge.
