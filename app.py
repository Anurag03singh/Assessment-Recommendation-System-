"""
Entry point for Railway deployment - Minimal version
"""
from backend.main_minimal import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
