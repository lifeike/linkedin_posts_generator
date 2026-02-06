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
from crawlers import FullstackCrawler, DockerCrawler, AWSCrawler
from post_generator import PostGenerator


class LinkedInPostApp:
    """Main application orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self.config.validate()
        
        self.fullstack = FullstackCrawler()
        self.docker = DockerCrawler()
        self.aws = AWSCrawler()
        self.generator = PostGenerator(self.config.openai_api_key, self.config.custom_hashtags)
        self.log_messages = []  # Store log messages for meta.txt
    
    def log(self, message: str):
        """Log message to both console and meta file"""
        print(message)
        self.log_messages.append(message)
    
    def run(self):
        """Run the complete workflow"""
        start_time = datetime.now()
        
        self.log("=" * 70)
        self.log("LinkedIn Post Generator")
        self.log("=" * 70)
        self.log(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("\nCrawling three fixed blog sources:")
        self.log("  • Fullstack Labs Blog")
        self.log("  • Docker Blog")
        self.log("  • AWS DevOps Blog")
        
        # Crawl all three blogs
        all_articles = []
        
        # Crawl Fullstack
        self.log("\n" + "=" * 70)
        self.log("Crawling Fullstack Blog")
        self.log("=" * 70)
        fullstack_articles = self.fullstack.crawl()
        all_articles.extend(fullstack_articles)
        self.log(f"✓ Found {len(fullstack_articles)} articles from Fullstack")
        
        # Crawl Docker
        self.log("\n" + "=" * 70)
        self.log("Crawling Docker Blog")
        self.log("=" * 70)
        docker_articles = self.docker.crawl()
        all_articles.extend(docker_articles)
        self.log(f"✓ Found {len(docker_articles)} articles from Docker")
        
        # Crawl AWS
        self.log("\n" + "=" * 70)
        self.log("Crawling AWS DevOps Blog")
        self.log("=" * 70)
        aws_articles = self.aws.crawl()
        all_articles.extend(aws_articles)
        self.log(f"✓ Found {len(aws_articles)} articles from AWS DevOps")
        
        self.log(f"\n{'=' * 70}")
        self.log(f"Total articles found: {len(all_articles)}")
        self.log('=' * 70)
        
        if not all_articles:
            self.log("\n❌ No articles found from any blog")
            self.save_meta()
            return
        
        # Generate posts for all articles
        self.log(f"\n{'=' * 70}")
        self.log(f"Generating LinkedIn Posts")
        self.log('=' * 70)
        
        results = self.generate_posts(all_articles)
        
        if results:
            # Save results
            self.save_results(results)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.log(f"\n{'=' * 70}")
            self.log(f"✅ COMPLETED! Generated {len(results)} LinkedIn posts")
            self.log('=' * 70)
            self.log(f"\nBreakdown by source:")
            
            # Count by source
            sources = {}
            for result in results:
                source = result.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            
            for source, count in sources.items():
                self.log(f"  • {source}: {count} posts")
            
            self.log(f"\nFiles created:")
            self.log(f"  📄 {self.config.output_file}")
            self.log(f"  📄 output/meta.txt")
            self.log(f"\nCompleted at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.log(f"Total duration: {duration:.1f} seconds")
        else:
            self.log("\n❌ No posts generated")
        
        # Save meta file
        self.save_meta()
    
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
                elif article['source'] == 'Docker':
                    content = self.docker.extract_content(article['url'])
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
        """Save results to TXT file grouped by source with easy copy-paste format"""
        output_file = self.config.output_file
        
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Group results by source
        grouped = {}
        for result in results:
            source = result['source']
            if source not in grouped:
                grouped[source] = []
            grouped[source].append(result)
        
        # Save as TXT grouped by category
        with open(output_file, 'w', encoding='utf-8') as f:
            for source in ['Fullstack', 'Docker', 'AWS DevOps']:
                if source not in grouped:
                    continue
                
                posts = grouped[source]
                
                # Category header
                f.write(f"{'=' * 70}\n")
                f.write(f"{source.upper()} POSTS ({len(posts)})\n")
                f.write(f"{'=' * 70}\n\n")
                
                # Write posts for this category
                for result in posts:
                    f.write(result['linkedin_post'])
                    f.write(f"\n\n{'- ' * 35}\n\n")
                
                f.write("\n")
        
        self.log(f"\n✓ Saved {len(results)} posts to {output_file}")
    
    def save_meta(self):
        """Save meta information (log messages) to meta.txt"""
        meta_file = "output/meta.txt"
        
        # Create output directory if it doesn't exist
        Path("output").mkdir(parents=True, exist_ok=True)
        
        with open(meta_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_messages))
        
        print(f"✓ Saved execution log to {meta_file}")


def main():
    """Entry point"""
    app = LinkedInPostApp()
    app.run()


if __name__ == "__main__":
    main()
