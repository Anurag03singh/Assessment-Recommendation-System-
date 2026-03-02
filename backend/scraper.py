"""
SHL Product Catalog Scraper
Crawls https://www.shl.com/solutions/products/product-catalog/
Extracts Individual Test Solutions (not pre-packaged job solutions)
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re


class SHLScraper:
    def __init__(self):
        self.base_url = "https://www.shl.com"
        self.catalog_url = f"{self.base_url}/solutions/products/product-catalog/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse HTML page"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    
    def extract_test_type(self, text: str) -> str:
        """Determine if test is K (Knowledge) or P (Personality)"""
        text_lower = text.lower()
        
        # P indicators
        p_keywords = ['personality', 'behavior', 'motivation', 'opq', 'mq', 
                      'occupational personality', 'behavioral', 'culture fit']
        
        # K indicators
        k_keywords = ['cognitive', 'ability', 'aptitude', 'skill', 'technical',
                      'numerical', 'verbal', 'knowledge', 'competency']
        
        p_score = sum(1 for kw in p_keywords if kw in text_lower)
        k_score = sum(1 for kw in k_keywords if kw in text_lower)
        
        return 'P' if p_score > k_score else 'K'
    
    def scrape_catalog(self) -> List[Dict]:
        """Main scraping logic"""
        print("Fetching catalog page...")
        soup = self.fetch_page(self.catalog_url)
        
        assessments = []
        
        # Find all assessment cards/items
        # Adjust selectors based on actual HTML structure
        items = soup.find_all(['div', 'article'], class_=re.compile(r'product|assessment|solution|card'))
        
        for item in items:
            try:
                # Extract assessment details
                name_elem = item.find(['h2', 'h3', 'h4', 'a'])
                if not name_elem:
                    continue
                
                name = name_elem.get_text(strip=True)
                
                # Skip pre-packaged job solutions
                if any(skip in name.lower() for skip in ['job solution', 'pre-packaged', 'bundle']):
                    continue
                
                # Get URL
                link = item.find('a', href=True)
                url = link['href'] if link else ""
                if url and not url.startswith('http'):
                    url = self.base_url + url
                
                # Get description
                desc_elem = item.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt'))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract metadata
                full_text = item.get_text()
                
                assessment = {
                    "assessment_name": name,
                    "url": url,
                    "test_type": self.extract_test_type(full_text),
                    "description": description,
                    "skills": self.extract_skills(full_text),
                    "job_level": self.extract_job_level(full_text),
                    "duration": self.extract_duration(full_text),
                    "category": self.extract_category(full_text)
                }
                
                assessments.append(assessment)
                
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue
        
        print(f"Scraped {len(assessments)} assessments")
        return assessments
    
    def extract_skills(self, text: str) -> str:
        """Extract skills mentioned"""
        skills = []
        skill_keywords = ['numerical', 'verbal', 'logical', 'mechanical', 'spatial',
                         'leadership', 'communication', 'problem solving', 'analytical']
        for skill in skill_keywords:
            if skill in text.lower():
                skills.append(skill.title())
        return ", ".join(skills) if skills else "General"
    
    def extract_job_level(self, text: str) -> str:
        """Extract job level"""
        text_lower = text.lower()
        if 'graduate' in text_lower or 'entry' in text_lower:
            return "Entry Level"
        elif 'manager' in text_lower or 'leadership' in text_lower:
            return "Manager"
        elif 'executive' in text_lower or 'senior' in text_lower:
            return "Senior"
        return "All Levels"
    
    def extract_duration(self, text: str) -> str:
        """Extract test duration"""
        duration_match = re.search(r'(\d+)\s*(min|minute|hour)', text.lower())
        if duration_match:
            return f"{duration_match.group(1)} {duration_match.group(2)}"
        return "Varies"
    
    def extract_category(self, text: str) -> str:
        """Extract assessment category"""
        text_lower = text.lower()
        if 'cognitive' in text_lower or 'ability' in text_lower:
            return "Cognitive Ability"
        elif 'personality' in text_lower:
            return "Personality"
        elif 'skill' in text_lower or 'technical' in text_lower:
            return "Technical Skills"
        return "General Assessment"
    
    def save_to_json(self, assessments: List[Dict], filepath: str = "data/shl_catalog.json"):
        """Save scraped data to JSON"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(assessments, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(assessments)} assessments to {filepath}")


if __name__ == "__main__":
    scraper = SHLScraper()
    assessments = scraper.scrape_catalog()
    
    if len(assessments) < 50:
        print("\n⚠️  WARNING: Only scraped {len(assessments)} assessments.")
        print("The actual catalog has 377+ Individual Test Solutions.")
        print("You may need to use Selenium for dynamic content or adjust selectors.")
    
    scraper.save_to_json(assessments)
