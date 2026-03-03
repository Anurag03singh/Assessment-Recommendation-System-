"""
Build assessment catalog from the provided dataset
Extracts unique URLs from training data and creates catalog
"""
import json
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time

def extract_unique_urls(train_file="data/train-set.json"):
    """Extract unique assessment URLs from training data"""
    print("Loading training data...")
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    
    # Extract unique URLs
    urls = set()
    query_to_urls = defaultdict(list)
    
    for item in train_data:
        query = item['Query']
        url = item['Assessment_url']
        urls.add(url)
        query_to_urls[query].append(url)
    
    print(f"Found {len(urls)} unique assessment URLs")
    print(f"Found {len(query_to_urls)} unique queries")
    
    return list(urls), dict(query_to_urls)


def scrape_assessment(url, timeout=10):
    """Scrape assessment details from URL"""
    try:
        print(f"  Scraping: {url}")
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract assessment name from title or h1
        name = None
        if soup.find('h1'):
            name = soup.find('h1').get_text(strip=True)
        elif soup.find('title'):
            name = soup.find('title').get_text(strip=True)
        
        # Extract description from meta or first paragraph
        description = ""
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
        elif soup.find('p'):
            description = soup.find('p').get_text(strip=True)
        
        # Try to extract duration, test type, etc.
        # This is a best-effort extraction
        text_content = soup.get_text()
        
        # Look for duration patterns
        duration = 60  # default
        if 'minutes' in text_content.lower():
            import re
            duration_match = re.search(r'(\d+)\s*minutes?', text_content, re.IGNORECASE)
            if duration_match:
                duration = int(duration_match.group(1))
        
        # Determine test type based on content
        test_types = []
        content_lower = text_content.lower()
        
        if any(word in content_lower for word in ['programming', 'coding', 'technical', 'java', 'python', 'sql']):
            test_types.append("Knowledge & Skills")
        if any(word in content_lower for word in ['personality', 'behavior', 'behaviour', 'opq']):
            test_types.append("Personality & Behaviour")
        if any(word in content_lower for word in ['competenc', 'skill']):
            if "Competencies" not in test_types:
                test_types.append("Competencies")
        if any(word in content_lower for word in ['cognitive', 'aptitude', 'reasoning', 'numerical', 'verbal']):
            test_types.append("Ability & Aptitude")
        
        if not test_types:
            test_types = ["Knowledge & Skills"]  # default
        
        return {
            "assessment_name": name or url.split('/')[-2].replace('-', ' ').title(),
            "url": url,
            "adaptive_support": "No",  # default
            "description": description[:500] if description else "Assessment details",
            "duration": duration,
            "remote_support": "Yes",  # default
            "test_type": test_types
        }
    
    except Exception as e:
        print(f"  ⚠️  Error scraping {url}: {e}")
        # Return minimal data
        return {
            "assessment_name": url.split('/')[-2].replace('-', ' ').title(),
            "url": url,
            "adaptive_support": "No",
            "description": "SHL Assessment",
            "duration": 60,
            "remote_support": "Yes",
            "test_type": ["Knowledge & Skills"]
        }


def build_catalog(urls, output_file="data/shl_catalog.json"):
    """Build catalog by scraping all URLs"""
    print(f"\nBuilding catalog from {len(urls)} URLs...")
    print("This may take a few minutes...\n")
    
    catalog = []
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]", end=" ")
        assessment = scrape_assessment(url)
        catalog.append(assessment)
        time.sleep(1)  # Be polite to the server
    
    # Save catalog
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Catalog saved to {output_file}")
    print(f"  Total assessments: {len(catalog)}")
    
    return catalog


def format_training_data(query_to_urls, output_file="data/labeled_queries.json"):
    """Format training data for evaluation"""
    print("\nFormatting training data...")
    
    train_queries = []
    for query, urls in query_to_urls.items():
        train_queries.append({
            "query": query,
            "relevant_assessments": urls
        })
    
    # Load test queries
    with open("data/test-set.json", 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    test_queries = [{"query": item['Query'], "relevant_assessments": []} for item in test_data]
    
    formatted_data = {
        "train_queries": train_queries,
        "test_queries": test_queries
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Training data saved to {output_file}")
    print(f"  Train queries: {len(train_queries)}")
    print(f"  Test queries: {len(test_queries)}")


if __name__ == "__main__":
    print("="*60)
    print("Building SHL Assessment Catalog from Dataset")
    print("="*60)
    
    # Step 1: Extract URLs
    urls, query_to_urls = extract_unique_urls()
    
    # Step 2: Build catalog
    catalog = build_catalog(urls)
    
    # Step 3: Format training data
    format_training_data(query_to_urls)
    
    print("\n" + "="*60)
    print("✅ Catalog building complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Review data/shl_catalog.json")
    print("2. Rebuild vector index: python embeddings.py")
    print("3. Run evaluation: python evaluate.py")
    print("4. Generate submission CSV: python export_csv.py")
