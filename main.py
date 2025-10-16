"""
LinkedIn Post Generator - Main Application
"""
import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from config import Config
from url_loader import URLLoader
from crawler import WebCrawler
from post_generator import PostGenerator


class LinkedInPostApp:
    """Main application orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self.config.validate()
        
        self.crawler = WebCrawler()
        self.generator = PostGenerator(self.config.openai_api_key)
    
    def run(self, urls_file: str = 'urls.txt'):
        """
        Run the complete workflow
        
        Args:
            urls_file: Path to file containing URLs (txt or json)
        """
        # Load URLs
        print("=" * 70)
        print("LinkedIn Post Generator")
        print("=" * 70)
        
        try:
            urls = URLLoader.load(urls_file)
            print(f"\n✓ Loaded {len(urls)} URLs from {urls_file}")
        except FileNotFoundError:
            print(f"\n❌ Error: {urls_file} not found")
            print("\nCreate one of these files:")
            print("  • urls.txt - One URL per line")
            print("  • urls.json - JSON array of URLs")
            return
        
        if not urls:
            print("❌ No URLs found in file")
            return
        
        # Process URLs
        results = self.process_urls(urls)
        
        if results:
            # Save results
            self.save_results(results)
            
            print(f"\n{'=' * 70}")
            print(f"✅ COMPLETED! Generated {len(results)} LinkedIn posts")
            print('=' * 70)
            print(f"\nFiles created:")
            print(f"  📄 {self.config.output_file}")
            print(f"  📄 {self.config.output_file.replace('.csv', '.json')}")
        else:
            print("\n❌ No posts generated")
    
    def process_urls(self, urls: List[str]) -> List[Dict]:
        """Process all URLs and generate posts"""
        all_results = []
        
        for url in urls:
            print(f"\n{'=' * 70}")
            print(f"Processing: {url}")
            print('=' * 70)
            
            # Crawl for articles
            articles = self.crawler.crawl_blog_page(
                url, 
                max_articles=self.config.max_articles_per_url
            )
            
            if not articles:
                print("⚠ No articles found, skipping...")
                continue
            
            # Generate posts for each article
            for i, article in enumerate(articles, 1):
                print(f"\n[{i}/{len(articles)}] {article['title'][:60]}...")
                
                # Optionally extract content
                content = ""
                if self.config.extract_content:
                    print("  → Extracting content...")
                    content = self.crawler.extract_content(article['url'])
                
                # Generate post
                print("  → Generating post...")
                post = self.generator.generate(article, content)
                
                # Store result
                result = {
                    'source_url': url,
                    'article_url': article['url'],
                    'article_title': article['title'],
                    'linkedin_post': post,
                    'generated_at': datetime.now().isoformat()
                }
                
                all_results.append(result)
                print(f"  ✓ Done ({len(post)} chars)")
                
                # Rate limiting
                time.sleep(1)
        
        return all_results
    
    def save_results(self, results: List[Dict]):
        """Save results to CSV and JSON files"""
        output_file = self.config.output_file
        
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n✓ Saved {len(results)} posts to {output_file}")
        
        # Save as JSON
        json_file = output_file.replace('.csv', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(results)} posts to {json_file}")


def main():
    """Entry point"""
    app = LinkedInPostApp()
    
    # Check for urls file
    urls_file = 'urls.txt'
    if Path('urls.json').exists():
        urls_file = 'urls.json'
    
    app.run(urls_file)


if __name__ == "__main__":
    main()
