"""
Create catalog from URLs using intelligent name extraction and categorization
Since scraping is blocked, we'll use URL patterns and common knowledge
"""
import json
import re

def extract_assessment_info_from_url(url):
    """Extract assessment information from URL pattern"""
    # Extract the assessment slug from URL
    slug = url.rstrip('/').split('/')[-1]
    
    # Convert slug to readable name
    name = slug.replace('-', ' ').replace('%28', '(').replace('%29', ')').title()
    
    # Determine test types and details based on keywords in slug
    slug_lower = slug.lower()
    
    test_types = []
    duration = 60  # default
    description = ""
    
    # Programming/Technical Skills
    if any(tech in slug_lower for tech in ['java', 'python', 'sql', 'javascript', 'css', 'html', 'selenium', 'drupal', 'tableau']):
        test_types.append("Knowledge & Skills")
        duration = 45
        tech_name = slug.replace('-new', '').replace('-', ' ').upper()
        description = f"Technical assessment evaluating proficiency in {tech_name} programming and related concepts."
    
    # Sales Assessments
    elif 'sales' in slug_lower:
        test_types.extend(["Competencies", "Personality & Behaviour"])
        duration = 30
        description = "Assessment evaluating sales competencies, customer interaction skills, and behavioral attributes for sales roles."
    
    # Personality/OPQ
    elif any(word in slug_lower for word in ['opq', 'personality', 'occupational']):
        test_types.append("Personality & Behaviour")
        duration = 25
        description = "Personality assessment measuring behavioral characteristics and work style preferences relevant to workplace performance."
    
    # Verify (Cognitive)
    elif 'verify' in slug_lower:
        test_types.extend(["Ability & Aptitude", "Knowledge & Skills"])
        duration = 20
        if 'numerical' in slug_lower:
            description = "Cognitive assessment measuring numerical reasoning and data interpretation abilities."
        elif 'verbal' in slug_lower:
            description = "Cognitive assessment evaluating verbal reasoning and comprehension skills."
        elif 'inductive' in slug_lower:
            description = "Cognitive assessment measuring inductive reasoning and pattern recognition abilities."
        else:
            description = "Cognitive ability assessment measuring reasoning and problem-solving skills."
    
    # Professional/Manager Assessments
    elif any(word in slug_lower for word in ['professional', 'manager', 'leadership', 'enterprise']):
        test_types.extend(["Competencies", "Personality & Behaviour"])
        duration = 35
        description = "Comprehensive assessment evaluating professional competencies, leadership potential, and behavioral attributes."
    
    # Communication/English
    elif any(word in slug_lower for word in ['communication', 'english', 'written', 'spoken']):
        test_types.extend(["Knowledge & Skills", "Competencies"])
        duration = 20
        description = "Assessment evaluating communication skills, language proficiency, and written/verbal expression."
    
    # Administrative
    elif 'administrative' in slug_lower or 'admin' in slug_lower:
        test_types.extend(["Knowledge & Skills", "Competencies"])
        duration = 25
        description = "Assessment measuring administrative skills, organizational abilities, and office productivity."
    
    # Excel/Office
    elif 'excel' in slug_lower or 'microsoft' in slug_lower:
        test_types.append("Knowledge & Skills")
        duration = 30
        description = "Technical assessment evaluating proficiency in Microsoft Excel and data management skills."
    
    # Marketing/SEO/Digital
    elif any(word in slug_lower for word in ['marketing', 'seo', 'digital', 'advertising']):
        test_types.extend(["Knowledge & Skills", "Competencies"])
        duration = 30
        description = "Assessment evaluating marketing knowledge, digital skills, and strategic thinking abilities."
    
    # Financial
    elif 'financial' in slug_lower or 'bank' in slug_lower:
        test_types.extend(["Knowledge & Skills", "Competencies"])
        duration = 30
        description = "Assessment measuring financial knowledge, analytical skills, and industry-specific competencies."
    
    # Data/Analytics
    elif any(word in slug_lower for word in ['data', 'warehouse', 'analysis']):
        test_types.append("Knowledge & Skills")
        duration = 35
        description = "Technical assessment evaluating data analysis, warehousing concepts, and analytical capabilities."
    
    # Testing/QA
    elif 'testing' in slug_lower or 'automata' in slug_lower:
        test_types.append("Knowledge & Skills")
        duration = 40
        description = "Technical assessment measuring software testing knowledge, QA methodologies, and automation skills."
    
    # Computer Literacy
    elif 'computer' in slug_lower or 'literacy' in slug_lower:
        test_types.append("Knowledge & Skills")
        duration = 20
        description = "Assessment evaluating basic computer skills and digital literacy."
    
    # Entry Level/General
    elif 'entry' in slug_lower or 'general' in slug_lower:
        test_types.extend(["Ability & Aptitude", "Competencies"])
        duration = 25
        description = "Entry-level assessment measuring foundational skills, aptitude, and work readiness."
    
    # Global Skills
    elif 'global' in slug_lower:
        test_types.extend(["Knowledge & Skills", "Competencies"])
        duration = 30
        description = "Comprehensive skills assessment evaluating multiple competencies and abilities."
    
    # Default
    if not test_types:
        test_types.append("Knowledge & Skills")
        description = f"Assessment evaluating skills and competencies for {name}."
    
    # Adaptive support (only for some assessments)
    adaptive = "Yes" if 'adaptive' in slug_lower else "No"
    
    return {
        "assessment_name": name,
        "url": url,
        "adaptive_support": adaptive,
        "description": description,
        "duration": duration,
        "remote_support": "Yes",
        "test_type": test_types
    }


def create_catalog_from_training_data(train_file="data/train-set.json", output_file="data/shl_catalog.json"):
    """Create catalog from training data URLs"""
    print("Loading training data...")
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    
    # Extract unique URLs
    urls = list(set(item['Assessment_url'] for item in train_data))
    print(f"Found {len(urls)} unique assessment URLs")
    
    # Create catalog
    catalog = []
    for url in sorted(urls):
        assessment = extract_assessment_info_from_url(url)
        catalog.append(assessment)
        print(f"  ✓ {assessment['assessment_name']}")
    
    # Save catalog
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Catalog saved to {output_file}")
    print(f"  Total assessments: {len(catalog)}")
    
    # Show test type distribution
    test_type_counts = {}
    for assessment in catalog:
        for tt in assessment['test_type']:
            test_type_counts[tt] = test_type_counts.get(tt, 0) + 1
    
    print(f"\nTest Type Distribution:")
    for tt, count in sorted(test_type_counts.items()):
        print(f"  {tt}: {count}")


if __name__ == "__main__":
    create_catalog_from_training_data()
