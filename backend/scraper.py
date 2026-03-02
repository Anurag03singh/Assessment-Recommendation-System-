"""
SHL Product Catalog Scraper
Crawls https://www.shl.com/solutions/products/product-catalog/
Extracts Individual Test Solutions (not pre-packaged job solutions)
Target: 377+ individual test solutions
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class SHLScraper:
    def __init__(self, use_selenium: bool = False):
        self.base_url = "https://www.shl.com"
        self.catalog_url = f"{self.base_url}/solutions/products/product-catalog/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.use_selenium = use_selenium
        self.driver = None
    
    def init_selenium(self):
        """Initialize Selenium WebDriver for dynamic content"""
        if self.driver:
            return
        
        print("Initializing Selenium WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ Selenium initialized")
        except Exception as e:
            print(f"⚠️  Selenium initialization failed: {e}")
            print("Falling back to requests library")
            self.use_selenium = False
    
    def close_selenium(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse HTML page"""
        if self.use_selenium:
            if not self.driver:
                self.init_selenium()
            
            if self.driver:
                try:
                    self.driver.get(url)
                    # Wait for content to load
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(2)  # Additional wait for dynamic content
                    return BeautifulSoup(self.driver.page_source, 'html.parser')
                except Exception as e:
                    print(f"Selenium fetch failed: {e}, falling back to requests")
        
        # Fallback to requests
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
    import sys
    
    # Check if user wants to use Selenium
    use_selenium = '--selenium' in sys.argv or '-s' in sys.argv
    
    print("="*60)
    print("SHL CATALOG SCRAPER")
    print("="*60)
    print(f"Target: 377+ Individual Test Solutions")
    print(f"Method: {'Selenium (dynamic)' if use_selenium else 'Requests (static)'}")
    print()
    
    scraper = SHLScraper(use_selenium=use_selenium)
    
    try:
        assessments = scraper.scrape_catalog()
        
        print(f"\n{'='*60}")
        print(f"SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"Total assessments scraped: {len(assessments)}")
        
        if len(assessments) < 377:
            print(f"\n⚠️  WARNING: Only scraped {len(assessments)} assessments.")
            print(f"Expected: 377+ Individual Test Solutions")
            print(f"\nTroubleshooting:")
            print(f"1. Try with Selenium: python scraper.py --selenium")
            print(f"2. Check if website structure changed")
            print(f"3. Verify internet connection")
            print(f"4. Check CSS selectors in scraper.py")
        else:
            print(f"✓ Successfully scraped {len(assessments)} assessments")
        
        # Save to JSON
        scraper.save_to_json(assessments)
        
        # Show sample
        if assessments:
            print(f"\nSample assessment:")
            sample = assessments[0]
            print(f"  Name: {sample['assessment_name']}")
            print(f"  Type: {sample['test_type']}")
            print(f"  URL: {sample['url']}")
        
    finally:
        scraper.close_selenium()
