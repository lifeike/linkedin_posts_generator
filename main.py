"""
LinkedIn Post Generator - Main Application
Uses three fixed blog sources: Fullstack, Expo, and AWS DevOps
"""
import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from config import Config
from crawlers import FullstackCrawler, ExpoCrawler, AWSCrawler
from post_generator import PostGenerator


class LinkedInPostApp:
    """Main application orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self.config.validate()
        
        self.fullstack = FullstackCrawler()
        self.expo = ExpoCrawler()
        self.aws = AWSCrawler()
        self.generator = PostGenerator(self.config.openai_api_key)
    
    def run(self):
        """Run the complete workflow"""
        print("=" * 70)
        print("LinkedIn Post Generator")
        print("=" * 70)
        print("\nCrawling three fixed blog sources:")
        print("  • Fullstack Labs Blog")
        print("  • Expo Blog")
        print("  • AWS DevOps Blog")
        
        # Crawl all three blogs
        all_articles = []
        
        # Crawl Fullstack
        fullstack_articles = self.fullstack.crawl()
        all_articles.extend(fullstack_articles)
        
        # Crawl Expo
        expo_articles = self.expo.crawl()
        all_articles.extend(expo_articles)
        
        # Crawl AWS
        aws_articles = self.aws.crawl()
        all_articles.extend(aws_articles)
        
        print(f"\n{'=' * 70}")
        print(f"Total articles found: {len(all_articles)}")
        print('=' * 70)
        
        if not all_articles:
            print("\n❌ No articles found from any blog")
            return
        
        # Generate posts for all articles
        results = self.generate_posts(all_articles)
        
        if results:
            # Save results
            self.save_results(results)
            
            print(f"\n{'=' * 70}")
            print(f"✅ COMPLETED! Generated {len(results)} LinkedIn posts")
            print('=' * 70)
            print(f"\nBreakdown by source:")
            
            # Count by source
            sources = {}
            for result in results:
                source = result.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            
            for source, count in sources.items():
                print(f"  • {source}: {count} posts")
            
            print(f"\nFiles created:")
            print(f"  📄 {self.config.output_file}")
            print(f"  📄 {self.config.output_file.replace('.csv', '.json')}")
        else:
            print("\n❌ No posts generated")
    
    def generate_posts(self, articles: List[Dict]) -> List[Dict]:
        """Generate LinkedIn posts for all articles"""
        results = []
        
        print(f"\n{'=' * 70}")
        print(f"Generating LinkedIn Posts")
        print('=' * 70)
        
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] {article['source']}: {article['title'][:50]}...")
            
            # Optionally extract content
            content = ""
            if self.config.extract_content:
                print("  → Extracting content...")
                # Use the appropriate crawler based on source
                if article['source'] == 'Fullstack':
                    content = self.fullstack.extract_content(article['url'])
                elif article['source'] == 'Expo':
                    content = self.expo.extract_content(article['url'])
                elif article['source'] == 'AWS DevOps':
                    content = self.aws.extract_content(article['url'])
            
            # Generate post
            print("  → Generating post...")
            post = self.generator.generate(article, content)
            
            # Store result
            result = {
                'source': article['source'],
                'article_url': article['url'],
                'article_title': article['title'],
                'linkedin_post': post,
                'generated_at': datetime.now().isoformat()
            }
            
            results.append(result)
            print(f"  ✓ Done ({len(post)} chars)")
            
            # Rate limiting to avoid API throttling
            time.sleep(1)
        
        return results
    
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
    app.run()


if __name__ == "__main__":
    main()
