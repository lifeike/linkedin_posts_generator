"""
AWS DevOps Blog Crawler - Extract articles from AWS DevOps blog
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class AWSCrawler:
    """Crawl AWS DevOps blog and extract article information"""
    
    URL = "https://aws.amazon.com/blogs/devops/"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def crawl(self) -> List[Dict]:
        """
        Crawl AWS DevOps blog and extract all articles
        
        Returns:
            List of dicts with 'url', 'title', and 'source' keys
        """
        print(f"\n{'=' * 70}")
        print(f"Crawling AWS DevOps Blog")
        print('=' * 70)
        print(f"URL: {self.URL}")
        
        try:
            response = requests.get(self.URL, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # AWS blog typically uses article tags or specific classes
            # Try multiple selectors
            article_elements = soup.find_all('article')
            
            if article_elements:
                for article in article_elements:
                    # Find title and link within article
                    link = article.find('a', href=True)
                    if link:
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        # Also try h2/h3 for title if link text is short
                        if len(title) < 15:
                            heading = article.find(['h2', 'h3', 'h4'])
                            if heading:
                                title = heading.get_text(strip=True)
                        
                        if title and len(title) > 15 and href:
                            # Make absolute URL if needed
                            if href.startswith('/'):
                                absolute_url = f"https://aws.amazon.com{href}"
                            elif href.startswith('http'):
                                absolute_url = href
                            else:
                                continue
                            
                            # Avoid duplicates
                            if not any(a['url'] == absolute_url for a in articles):
                                articles.append({
                                    'url': absolute_url,
                                    'title': title,
                                    'source': 'AWS DevOps'
                                })
            else:
                # Fallback: find all links with /blogs/devops/ in href
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    href = link.get('href', '')
                    title = link.get_text(strip=True)
                    
                    if '/blogs/devops/' in href and title and len(title) > 15:
                        if href.startswith('/'):
                            absolute_url = f"https://aws.amazon.com{href}"
                        elif href.startswith('http'):
                            absolute_url = href
                        else:
                            continue
                        
                        # Avoid duplicates and main blog page
                        if (not any(a['url'] == absolute_url for a in articles) and 
                            absolute_url != self.URL):
                            articles.append({
                                'url': absolute_url,
                                'title': title,
                                'source': 'AWS DevOps'
                            })
            
            print(f"✓ Found {len(articles)} articles from AWS DevOps blog")
            
            if not articles:
                print("⚠ No articles found. The page structure may have changed.")
            
            return articles
            
        except Exception as e:
            print(f"❌ Error crawling AWS DevOps blog: {str(e)}")
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
