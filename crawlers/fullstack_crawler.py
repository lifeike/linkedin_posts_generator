"""
Fullstack Blog Crawler - Extract articles from Fullstack blog
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class FullstackCrawler:
    """Crawl Fullstack blog and extract article information"""
    
    URL = "https://www.fullstack.com/labs/resources/blog"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl(self) -> List[Dict]:
        """
        Crawl Fullstack blog and extract all articles
        
        Returns:
            List of dicts with 'url', 'title', and 'source' keys
        """
        print(f"\n{'=' * 70}")
        print(f"Crawling Fullstack Blog")
        print('=' * 70)
        print(f"URL: {self.URL}")
        
        try:
            response = requests.get(self.URL, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find article cards/links (adjust selectors based on site structure)
            article_links = soup.find_all('a', href=True)
            
            for link in article_links:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                # Filter for blog article links
                if ('/blog/' in href or href.startswith('/labs/resources/blog/')) and title and len(title) > 15:
                    # Make absolute URL
                    if href.startswith('/'):
                        absolute_url = f"https://www.fullstack.com{href}"
                    elif href.startswith('http'):
                        absolute_url = href
                    else:
                        continue
                    
                    # Avoid duplicates
                    if not any(a['url'] == absolute_url for a in articles):
                        articles.append({
                            'url': absolute_url,
                            'title': title,
                            'source': 'Fullstack'
                        })
            
            print(f"✓ Found {len(articles)} articles from Fullstack blog")
            
            if not articles:
                print("⚠ No articles found. The page structure may have changed.")
            
            return articles
            
        except Exception as e:
            print(f"❌ Error crawling Fullstack blog: {str(e)}")
            return []
    
    def extract_content(self, url: str) -> str:
        """
        Extract main content from an article URL
        
        Returns:
            Article content (first 300 words)
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()
            
            # Try to find main content
            main_selectors = ['article', 'main', '.post-content', '.blog-content', '.entry-content']
            content = ""
            
            for selector in main_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    content = main_content.get_text(separator=' ', strip=True)
                    break
            
            if not content:
                content = soup.get_text(separator=' ', strip=True)
            
            # Limit to first 300 words
            words = content.split()[:300]
            return ' '.join(words)
            
        except Exception as e:
            print(f"  ⚠ Could not extract content: {str(e)}")
            return ""
