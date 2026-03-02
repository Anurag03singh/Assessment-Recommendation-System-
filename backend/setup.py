"""
Setup script to initialize the system
Run this after installing requirements
"""
import os
import sys


def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import sentence_transformers
        import chromadb
        import requests
        import bs4
        print("✓ All required packages installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False


def create_directories():
    """Create necessary directories"""
    dirs = ['data', 'chroma_db']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✓ Created directory: {d}")


def run_scraper():
    """Run the scraper"""
    print("\n" + "="*50)
    print("STEP 1: Scraping SHL Catalog")
    print("="*50)
    
    response = input("\nRun scraper now? (y/n): ")
    if response.lower() == 'y':
        import scraper
        s = scraper.SHLScraper()
        assessments = s.scrape_catalog()
        s.save_to_json(assessments)
        
        if len(assessments) < 50:
            print("\n⚠️  WARNING: Only scraped {len(assessments)} assessments")
            print("You may need to:")
            print("1. Use Selenium for dynamic content")
            print("2. Adjust CSS selectors in scraper.py")
            print("3. Check if the website structure changed")
    else:
        print("Skipped. Run manually: python scraper.py")


def build_index():
    """Build the vector index"""
    print("\n" + "="*50)
    print("STEP 2: Building Vector Index")
    print("="*50)
    
    if not os.path.exists('data/shl_catalog.json'):
        print("✗ No catalog data found. Run scraper first.")
        return
    
    response = input("\nBuild index now? This may take a few minutes. (y/n): ")
    if response.lower() == 'y':
        import embeddings
        import json
        
        with open('data/shl_catalog.json', 'r') as f:
            assessments = json.load(f)
        
        em = embeddings.EmbeddingManager()
        em.build_index(assessments)
        print("✓ Index built successfully")
    else:
        print("Skipped. Run manually: python embeddings.py")


def create_sample_labeled_data():
    """Create sample labeled data structure"""
    print("\n" + "="*50)
    print("STEP 3: Labeled Data Setup")
    print("="*50)
    
    if os.path.exists('data/labeled_queries.json'):
        print("✓ Labeled data already exists")
        return
    
    print("\nCreating sample labeled data structure...")
    import evaluate
    evaluate.create_sample_labeled_data()
    print("\n⚠️  Replace with actual labeled queries from the assignment")


def main():
    print("SHL Assessment Recommender - Setup")
    print("="*50)
    
    if not check_requirements():
        sys.exit(1)
    
    create_directories()
    run_scraper()
    build_index()
    create_sample_labeled_data()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE")
    print("="*50)
    print("\nNext steps:")
    print("1. Add actual labeled queries to data/labeled_queries.json")
    print("2. Run evaluation: python evaluate.py")
    print("3. Start API: uvicorn main:app --reload")
    print("4. Test at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
