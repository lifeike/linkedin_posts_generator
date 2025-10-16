# LinkedIn Post Generator 🚀

Automatically crawl blog URLs and generate professional LinkedIn posts using AI.

## Features

✨ **Crawl Multiple Blogs** - Extract articles from blog pages automatically  
🤖 **AI-Powered Posts** - Generate engaging LinkedIn posts using OpenAI  
📁 **Flexible Input** - Load URLs from text or JSON files  
💾 **Multiple Formats** - Export to CSV and JSON  
🔒 **Secure** - API keys stored in `.env` file (not committed to git)

## Quick Start

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/linkedin-post-generator.git
cd linkedin-post-generator

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install openai requests beautifulsoup4
```

### 2. Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Add URLs

**Option A: Text file (urls.txt)**
```text
https://aws.amazon.com/blogs/aws/
https://www.lastweekinaws.com/blog/
```

**Option B: JSON file (urls.json)**
```json
{
  "urls": [
    "https://aws.amazon.com/blogs/aws/",
    "https://www.lastweekinaws.com/blog/"
  ]
}
```

### 4. Run

```bash
python main.py
```

## Project Structure

```
linkedin-post-generator/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── url_loader.py        # URL file reader
├── crawler.py           # Web crawler
├── post_generator.py    # AI post generator
├── .env                 # Environment variables (not in git)
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
├── urls.txt             # URL input file (create this)
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Configuration

Edit `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
MAX_ARTICLES_PER_URL=30        # Articles per URL
EXTRACT_CONTENT=false          # Extract full content (slower)
OUTPUT_FILE=linkedin_posts.csv # Output filename
```

## Output

The tool generates two files:

- **linkedin_posts.csv** - Spreadsheet format
- **linkedin_posts.json** - JSON format

Each post includes:
- Source URL
- Article URL
- Article title
- Generated LinkedIn post
- Timestamp

## API Costs

Using OpenAI GPT-3.5-turbo:
- ~$0.001-0.002 per post
- 30 posts ≈ $0.03-0.06
- 1000 posts ≈ $1-2

Very affordable! 💰

## Requirements

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Internet connection

## Troubleshooting

**No articles found?**
- Try using specific blog archive URLs
- Check if the site requires JavaScript (try simpler sites)
- Use individual article URLs instead

**API errors?**
- Verify your OpenAI API key in `.env`
- Check you have credits in your OpenAI account
- Ensure `.env` file is in the project root

**Import errors?**
```bash
uv pip install --upgrade openai requests beautifulsoup4
```

## Contributing

Pull requests welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use for personal or commercial projects!

## Support

Having issues? [Open an issue](https://github.com/yourusername/linkedin-post-generator/issues)

---

Made with ❤️ using Python and OpenAI
