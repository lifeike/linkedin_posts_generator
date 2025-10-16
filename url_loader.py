"""
URL Loader - Reads URLs from various file formats
"""
import json
from pathlib import Path
from typing import List


class URLLoader:
    """Load URLs from files"""
    
    @staticmethod
    def load_from_text(filepath: str) -> List[str]:
        """
        Load URLs from text file (one URL per line)
        
        Example urls.txt:
            https://aws.amazon.com/blogs/aws/
            https://www.lastweekinaws.com/blog/
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        urls = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    urls.append(line)
        
        return urls
    
    @staticmethod
    def load_from_json(filepath: str) -> List[str]:
        """
        Load URLs from JSON file
        
        Example urls.json:
            {
              "urls": [
                "https://aws.amazon.com/blogs/aws/",
                "https://www.lastweekinaws.com/blog/"
              ]
            }
        
        Or simple array:
            [
              "https://aws.amazon.com/blogs/aws/",
              "https://www.lastweekinaws.com/blog/"
            ]
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both formats: {"urls": [...]} or [...]
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'urls' in data:
            return data['urls']
        else:
            raise ValueError("JSON must be an array or object with 'urls' key")
    
    @staticmethod
    def load(filepath: str) -> List[str]:
        """
        Auto-detect format and load URLs
        
        Supports: .txt, .json
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.txt':
            return URLLoader.load_from_text(filepath)
        elif suffix == '.json':
            return URLLoader.load_from_json(filepath)
        else:
            # Try text format as fallback
            return URLLoader.load_from_text(filepath)
