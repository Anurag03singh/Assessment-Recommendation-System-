"""
Setup Verification Script
Run this to verify all files are in place before starting development
"""
import os
import sys

def check_file(path, description):
    """Check if a file exists"""
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {path}")
    return exists

def check_directory(path, description):
    """Check if a directory exists"""
    exists = os.path.isdir(path)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print("="*70)
    print("SHL ASSESSMENT RECOMMENDER - SETUP VERIFICATION")
    print("="*70)
    
    checks = []
    
    print("\n📁 Backend Files:")
    checks.append(check_file("backend/main.py", "FastAPI application"))
    checks.append(check_file("backend/scraper.py", "Web scraper"))
    checks.append(check_file("backend/embeddings.py", "Embedding manager"))
    checks.append(check_file("backend/recommender.py", "Recommendation engine"))
    checks.append(check_file("backend/evaluate.py", "Evaluation framework"))
    checks.append(check_file("backend/export_csv.py", "CSV export"))
    checks.append(check_file("backend/test_system.py", "System tests"))
    checks.append(check_file("backend/setup.py", "Setup wizard"))
    checks.append(check_file("backend/quick_test.py", "Quick test"))
    checks.append(check_file("backend/requirements.txt", "Python dependencies"))
    checks.append(check_file("backend/Dockerfile", "Docker config"))
    
    print("\n📁 Backend Data:")
    checks.append(check_directory("backend/data", "Data directory"))
    checks.append(check_file("backend/data/sample_catalog.json", "Sample catalog"))
    checks.append(check_file("backend/data/sample_labeled_queries.json", "Sample queries"))
    
    print("\n📁 Frontend Files:")
    checks.append(check_file("frontend/package.json", "NPM package config"))
    checks.append(check_file("frontend/vite.config.js", "Vite config"))
    checks.append(check_file("frontend/tailwind.config.js", "Tailwind config"))
    checks.append(check_file("frontend/index.html", "HTML entry point"))
    checks.append(check_file("frontend/src/App.jsx", "React main component"))
    checks.append(check_file("frontend/src/main.jsx", "React entry point"))
    checks.append(check_file("frontend/src/index.css", "CSS with Tailwind"))
    checks.append(check_file("frontend/.env.example", "Environment example"))
    
    print("\n📁 Documentation:")
    checks.append(check_file("README.md", "Project README"))
    checks.append(check_file("QUICKSTART.md", "Quick start guide"))
    checks.append(check_file("TECHNICAL_DOCUMENT.md", "Technical document"))
    checks.append(check_file("DEPLOYMENT.md", "Deployment guide"))
    checks.append(check_file("WORKFLOW.md", "Development workflow"))
    checks.append(check_file("CHECKLIST.md", "Implementation checklist"))
    checks.append(check_file("PROJECT_SUMMARY.md", "Project summary"))
    
    print("\n📁 Configuration:")
    checks.append(check_file(".gitignore", "Git ignore file"))
    
    print("\n" + "="*70)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"VERIFICATION COMPLETE: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All files present! You're ready to start.")
        print("\nNext steps:")
        print("1. cd backend")
        print("2. pip install -r requirements.txt")
        print("3. python quick_test.py")
        print("\nSee QUICKSTART.md for detailed instructions.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} files missing!")
        print("Some files may not have been created properly.")
        print("Please check the setup and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
