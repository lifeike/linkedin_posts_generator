# LinkedIn Post Generator 🚀

Automatically crawl three tech blogs and generate professional LinkedIn posts using AI.

## Features

✨ **Three Fixed Blog Sources** - Crawls Fullstack Labs, Docker, and AWS DevOps blogs  
🤖 **AI-Powered Posts** - Generate engaging LinkedIn posts using OpenAI GPT-3.5  
📡 **RSS Feed Support** - Stable extraction using RSS feeds where available  
🔒 **Secure** - API keys stored in `.env` file (not committed to git)

## Blog Sources

The tool automatically crawls these three blogs:

1. **Fullstack Labs** - https://www.fullstack.com/labs/resources/blog
2. **Docker** - https://www.docker.com/blog/
3. **AWS DevOps** - https://aws.amazon.com/blogs/devops/

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/linkedin-post-generator.git
cd linkedin-post-generator

# Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

Add your API key to `.env`:
```bash
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### 3. Run

```bash
python3 main.py
```

That's it! The tool will crawl all three blogs and generate LinkedIn posts automatically.

## Project Structure

```
linkedin-post-generator/
├── crawlers/
│   ├── __init__.py
│   ├── fullstack_crawler.py    # Fullstack Labs crawler
│   ├── docker_crawler.py        # Docker blog crawler
│   └── aws_crawler.py           # AWS DevOps crawler
├── main.py                      # Main application entry point
├── config.py                    # Configuration management
├── post_generator.py            # AI post generator
├── output/                      # Generated posts (created automatically)
│   ├── linkedin_posts.csv
│   └── linkedin_posts.json
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Configuration

Edit `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
MAX_ARTICLES_PER_URL=30        # Articles per blog (default: 30)
EXTRACT_CONTENT=false          # Extract full content (slower, default: false)
OUTPUT_FILE=output/linkedin_posts.csv  # Output filename
```

### Configuration Options

- **OPENAI_API_KEY** (required): Your OpenAI API key
- **MAX_ARTICLES_PER_URL** (optional): Maximum articles to process per blog (default: 30)
- **EXTRACT_CONTENT** (optional): Set to `true` to extract full article content for better posts (slower)
- **OUTPUT_FILE** (optional): Path and filename for output CSV (default: `output/linkedin_posts.csv`)

## Output

The tool generates two files in the `output/` directory:

- **linkedin_posts.csv** - Spreadsheet format with all posts
- **linkedin_posts.json** - JSON format for programmatic use

Each post includes:
- Source (Fullstack, Expo, or AWS DevOps)
- Article URL
- Article title
- Generated LinkedIn post
- Timestamp

### Example Output

```
======================================================================
✅ COMPLETED! Generated 45 LinkedIn posts
======================================================================

Breakdown by source:
  • Fullstack: 12 posts
  • Docker: 20 posts
  • AWS DevOps: 13 posts

Files created:
  📄 output/linkedin_posts.csv
  📄 output/linkedin_posts.json
```

## API Costs

Using OpenAI GPT-3.5-turbo:
- ~$0.001-0.002 per post
- 30 posts ≈ $0.03-0.06
- 100 posts ≈ $0.10-0.20

Very affordable! 💰

## Requirements

- Python 3.10+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Internet connection

### Python Dependencies

All dependencies are listed in `requirements.txt`:
- `openai>=1.0.0` - OpenAI API client
- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.0` - HTML parsing
- `lxml>=4.9.0` - XML/HTML parser

## How It Works

1. **Crawl Blogs** - Each crawler extracts articles from its specific blog
   - Fullstack: Parses HTML structure
   - Docker: Parses HTML structure
   - AWS DevOps: Parses HTML structure

2. **Generate Posts** - For each article:
   - Sends article title (and content if enabled) to OpenAI
   - GPT-3.5 generates a professional LinkedIn post
   - Post includes hook, key takeaways, and hashtags

3. **Save Results** - Exports all posts to CSV and JSON formats

## Troubleshooting

**No articles found from a blog?**
- Check your internet connection
- The blog's HTML structure may have changed
- Check the crawler file for that specific blog

**API errors?**
- Verify your OpenAI API key in `.env`
- Check you have credits in your OpenAI account
- Ensure `.env` file is in the project root directory

**Import errors?**
```bash
pip install -r requirements.txt
```

**Permission denied error?**
- Make sure `OUTPUT_FILE` in `.env` uses a relative path like `output/linkedin_posts.csv`
- Don't use absolute paths like `/output/linkedin_posts.csv`

**Rate limiting?**
- The script includes 1-second delays between API calls
- If you hit rate limits, reduce `MAX_ARTICLES_PER_URL` in `.env`

## Customization

### Adding a New Blog

1. Create a new crawler in `crawlers/` (e.g., `your_blog_crawler.py`)
2. Implement the `crawl()` and `extract_content()` methods
3. Add the import to `crawlers/__init__.py`
4. Update `main.py` to use the new crawler

### Changing the Prompt

Edit `post_generator.py` to customize the AI prompt for different post styles.

## Contributing

Pull requests welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use for personal or commercial projects!

## Support

Having issues? [Open an issue](https://github.com/yourusername/linkedin-post-generator/issues) , Inspired by [linkedin-post-automator](https://github.com/CRAKZOR/linkedin-post-automator)

