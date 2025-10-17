"""
Expo Blog Crawler - Extract articles from React Native blog via RSS
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import xml.etree.ElementTree as ET


class ExpoCrawler:
    """Crawl React Native blog via RSS feed"""
    
    URL = "https://reactnative.dev/blog"
    RSS_URL = "https://reactnative.dev/blog/rss.xml"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl(self) -> List[Dict]:
        """
        Crawl React Native blog via RSS feed
        
        Returns:
            List of dicts with 'url', 'title', and 'source' keys
        """
        print(f"\n{'=' * 70}")
        print(f"Crawling React Native Blog")
        print('=' * 70)
        print(f"RSS Feed: {self.RSS_URL}")
        
        try:
            response = requests.get(self.RSS_URL, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            articles = []
            
            # Parse RSS XML
            root = ET.fromstring(response.content)
            
            # RSS 2.0 format - items are in channel/item
            for item in root.findall('.//item'):
                title_elem = item.find('title')
                link_elem = item.find('link')
                
                if title_elem is not None and link_elem is not None:
                    title = title_elem.text
                    url = link_elem.text
                    
                    if title and url:
                        articles.append({
                            'url': url.strip(),
                            'title': title.strip(),
                            'source': 'Expo'
                        })
            
            print(f"✓ Found {len(articles)} articles from React Native blog")
            
            if not articles:
                print("⚠ No articles found in RSS feed.")
            
            return articles
            
        except ET.ParseError as e:
            print(f"❌ Error parsing RSS feed: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Error crawling React Native blog: {str(e)}")
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
