"""
Post Generator - Generate LinkedIn posts using AI
"""
from openai import OpenAI
from typing import Dict


class PostGenerator:
    """Generate LinkedIn posts using OpenAI"""
    
    def __init__(self, api_key: str, custom_hashtags: str = ""):
        """
        Initialize the post generator
        
        Args:
            api_key: OpenAI API key
            custom_hashtags: Custom hashtags to append to posts
        """
        self.client = OpenAI(api_key=api_key)
        self.custom_hashtags = custom_hashtags
    
    def generate(self, article: Dict, content: str = "") -> str:
        """
        Generate a LinkedIn post for an article
        
        Args:
            article: Dict with 'title' and 'url' keys
            content: Optional article content for better posts
            
        Returns:
            Generated LinkedIn post text with custom hashtags
        """
        prompt = self._build_prompt(article, content)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=450
            )
            post = response.choices[0].message.content.strip()
            
            # Append custom hashtags if provided
            if self.custom_hashtags:
                post = f"{post}\n\n{self.custom_hashtags}"
            
            return post
        except Exception as e:
            return f"Error generating post: {str(e)}"
    
    def _build_prompt(self, article: Dict, content: str) -> str:
        """Build the prompt for AI generation"""
        content_section = ""
        if content:
            content_section = f"\nContent Preview: {content[:400]}"
        
        return f"""Create a professional LinkedIn post about this article.

Title: {article['title']}
URL: {article['url']}{content_section}

STRICT FORMAT REQUIREMENTS:
1. Start with an attention-grabbing hook (1-2 sentences with an emoji)
2. Add a blank line
3. Write EXACTLY 3 key takeaways using this format:
   1️⃣ First takeaway
   2️⃣ Second takeaway  
   3️⃣ Third takeaway
4. Add a blank line
5. End with "Read more: [URL]"
6. Add a blank line
7. Add 3-5 relevant hashtags (topic-specific, not role-based)

STYLE:
- Professional yet conversational tone
- Each takeaway should be concise (1-2 lines max)
- Use bullet emojis (1️⃣ 2️⃣ 3️⃣) for takeaways
- Length: 150-250 words total

Write the LinkedIn post following this exact structure:"""
