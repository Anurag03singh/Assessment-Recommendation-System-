"""
Build ChromaDB embeddings before deployment
Run this locally before deploying to ensure vector DB is ready
"""
import os
import sys
import json

# Add backend to path
sys.path.insert(0, 'backend')

from embeddings_lite import EmbeddingManager

def main():
    print("=" * 60)
    print("Building ChromaDB Embeddings for Deployment")
    print("=" * 60)
    
    # Find catalog file
    possible_paths = [
        "backend/data/shl_catalog.json",
        "data/shl_catalog.json"
    ]
    
    catalog_file = None
    for path in possible_paths:
        if os.path.exists(path):
            catalog_file = path
            print(f"✓ Found catalog: {path}")
            break
    
    if not catalog_file:
        print("❌ Error: shl_catalog.json not found!")
        print("Searched in:", possible_paths)
        return False
    
    # Load catalog
    with open(catalog_file, 'r', encoding='utf-8') as f:
        assessments = json.load(f)
    
    print(f"✓ Loaded {len(assessments)} assessments")
    
    # Initialize embedding manager
    print("\n📦 Initializing embedding manager...")
    em = EmbeddingManager(db_path="./chroma_db")
    
    # Build index
    print("\n🔨 Building vector index...")
    print("This may take 1-2 minutes...")
    em.build_index(assessments)
    
    # Verify
    print("\n✅ Verifying index...")
    em.load_collection()
    count = em.collection.count()
    print(f"✓ Index contains {count} assessments")
    
    # Test search
    print("\n🧪 Testing search...")
    test_query = "Java developer with communication skills"
    results = em.search(test_query, k=5)
    print(f"✓ Search returned {len(results)} results")
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! ChromaDB is ready for deployment")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify 'chroma_db' folder exists")
    print("2. Deploy to your platform (Render, Railway, Fly.io)")
    print("3. Ensure chroma_db folder is included in deployment")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
