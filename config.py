"""
Configuration Manager - Loads settings from .env file
"""
import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration"""
    
    def __init__(self):
        self.load_env()
        
    def load_env(self):
        """Load environment variables from .env file"""
        env_path = Path('.env')
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment"""
        return os.getenv('OPENAI_API_KEY')
    
    @property
    def max_articles_per_url(self) -> int:
        """Maximum articles to process per URL"""
        return int(os.getenv('MAX_ARTICLES_PER_URL', '30'))
    
    @property
    def extract_content(self) -> bool:
        """Whether to extract full article content"""
        return os.getenv('EXTRACT_CONTENT', 'false').lower() == 'true'
    
    @property
    def output_file(self) -> str:
        """Output TXT filename"""
        return os.getenv('OUTPUT_FILE', 'output/linkedin_posts.txt')
    
    @property
    def custom_hashtags(self) -> str:
        """Custom hashtags to append to posts"""
        default_tags = '#SoftwareEngineer #Developer #FullStackDeveloper #AWS #ReactNative #CloudComputing #MobileDev'
        return os.getenv('CUSTOM_HASHTAGS', default_tags)
    
    def validate(self):
        """Validate required configuration"""
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please create a .env file with your API key."
            )
