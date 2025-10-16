"""
Web Crawler - Extract articles from blog pages
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin


class WebCrawler:
    """Crawl blog pages and extract article information"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl_blog_page(self, url: str, max_articles: int = 30) -> List[Dict]:
        """
        Crawl a blog page and extract article URLs and titles
        
        Returns:
            List of dicts with 'url' and 'title' keys
        """
        print(f"Crawling {url}...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find all article links
            all_article_links = soup.find_all('article')
            if all_article_links:
                for article in all_article_links[:max_articles * 2]:  # Get extra to filter
                    links = article.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        if title and len(title) > 10:
                            absolute_url = self._make_absolute_url(url, href)
                            articles.append({
                                'url': absolute_url,
                                'title': title
                            })
            
            # Remove duplicates while preserving order
            unique_articles = self._remove_duplicates(articles)[:max_articles]
            
            print(f"✓ Found {len(unique_articles)} articles")
            
            if not unique_articles:
                print("⚠ No articles found. Try a different URL or specific article links.")
            
            return unique_articles
            
        except Exception as e:
            print(f"❌ Error crawling {url}: {str(e)}")
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
            main_selectors = ['article', 'main', '.post-content', '.entry-content']
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
    
    @staticmethod
    def _make_absolute_url(base_url: str, href: str) -> str:
        """Convert relative URL to absolute"""
        if href.startswith('http'):
            return href
        return urljoin(base_url, href)
    
    @staticmethod
    def _remove_duplicates(articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles while preserving order"""
        seen = set()
        unique = []
        
        for article in articles:
            url = article['url']
            if url not in seen and url.startswith('http'):
                seen.add(url)
                unique.append(article)
        
        return unique
