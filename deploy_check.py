"""
Pre-Deployment Checklist Script
Verifies all requirements are met before deployment
"""
import os
import sys
import json

def check_file(path, description):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_directory(path, description):
    """Check if a directory exists and has content"""
    exists = os.path.exists(path) and os.path.isdir(path)
    if exists:
        files = os.listdir(path)
        has_content = len(files) > 0
        status = "✅" if has_content else "⚠️"
        print(f"{status} {description}: {path} ({len(files)} files)")
        return has_content
    else:
        print(f"❌ {description}: {path} (not found)")
        return False

def check_json_file(path, description):
    """Check if JSON file exists and is valid"""
    if not os.path.exists(path):
        print(f"❌ {description}: {path} (not found)")
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        count = len(data) if isinstance(data, list) else 1
        print(f"✅ {description}: {path} ({count} items)")
        return True
    except Exception as e:
        print(f"❌ {description}: {path} (invalid JSON: {e})")
        return False

def main():
    print("=" * 70)
    print("🔍 Pre-Deployment Checklist")
    print("=" * 70)
    
    checks = []
    
    print("\n📁 Core Files:")
    checks.append(check_file("backend/main_production.py", "Production main file"))
    checks.append(check_file("backend/embeddings_lite.py", "Lite embeddings"))
    checks.append(check_file("backend/recommender.py", "Recommender engine"))
    
    print("\n📦 Dependencies:")
    checks.append(check_file("backend/requirements-lite.txt", "Lite requirements"))
    checks.append(check_file("backend/requirements.txt", "Full requirements"))
    
    print("\n📊 Data Files:")
    checks.append(check_json_file("backend/data/shl_catalog.json", "Assessment catalog"))
    
    print("\n🗄️ Vector Database:")
    checks.append(check_directory("chroma_db", "ChromaDB folder"))
    
    print("\n⚙️ Configuration Files:")
    checks.append(check_file("render.yaml", "Render config"))
    checks.append(check_file("railway.json", "Railway config"))
    checks.append(check_file("fly.toml", "Fly.io config"))
    checks.append(check_file("Procfile", "Procfile"))
    
    print("\n📖 Documentation:")
    checks.append(check_file("DEPLOY_READY.md", "Deployment guide"))
    checks.append(check_file("DEPLOYMENT_OPTIMIZED.md", "Optimization guide"))
    
    print("\n" + "=" * 70)
    
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("=" * 70)
        print("\n🚀 Your project is ready for deployment!")
        print("\nNext steps:")
        print("1. Choose your platform (Render, Railway, or Fly.io)")
        print("2. Push code to GitHub (if using Render)")
        print("3. Follow instructions in DEPLOY_READY.md")
        print("\nRecommended: Deploy to Render for easiest setup")
        return True
    else:
        print(f"⚠️  CHECKS INCOMPLETE ({passed}/{total} - {percentage:.0f}%)")
        print("=" * 70)
        print("\n❌ Some requirements are missing!")
        
        if not os.path.exists("chroma_db") or not os.listdir("chroma_db"):
            print("\n🔨 Action Required: Build ChromaDB")
            print("Run: python build_embeddings.py")
        
        print("\nReview the checklist above and fix missing items.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
