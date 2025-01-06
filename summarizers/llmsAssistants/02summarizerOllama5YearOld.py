import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from typing import Optional, Dict, Any, Tuple

class OllamaConfig:
    """Configuration settings for Ollama API"""
    API_URL = "http://localhost:11434/api/generate"
    VERSION_URL = "http://localhost:11434/api/version"
    MODEL = "llama3.2:1b"
    HEADERS = {"Content-Type": "application/json"}

class WebScraper:
    """Handles all web scraping operations"""
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_page(self, url: str) -> requests.Response:
        """Fetch webpage content"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response

    def parse_html(self, content: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(content, 'html.parser')

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        return soup.title.string if soup.title else "No title found"

    def clean_body_content(self, soup: BeautifulSoup) -> str:
        """Clean and extract body content"""
        if not soup.body:
            return ""
            
        # Remove irrelevant elements
        for tag in soup.body.find_all(["script", "style", "img", "input"]):
            tag.decompose()
            
        return soup.body.get_text(separator="\n", strip=True)

class OllamaService:
    """Handles all Ollama API interactions"""
    def check_availability(self) -> bool:
        """Check if Ollama service is available"""
        try:
            response = requests.get(OllamaConfig.VERSION_URL)
            return response.status_code == 200
        except:
            return False

    def generate_summary(self, prompt: str) -> str:
        """Generate summary using Ollama"""
        payload = {
            "model": OllamaConfig.MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(
            OllamaConfig.API_URL,
            headers=OllamaConfig.HEADERS,
            json=payload
        )
        response.raise_for_status()
        return response.json().get("response", "No response content found.")

class PromptGenerator:
    """Handles creation of prompts for the AI model"""
    @staticmethod
    def create_system_prompt() -> str:
        return """You are an assistant that analyzes websites and provides summaries.
        Focus on relevant numeric data and explain it simply.
        Format your response using markdown with appropriate headers, lists, and emphasis."""

    @staticmethod
    def create_user_prompt(title: str, content: str) -> str:
        return f"""### System: {PromptGenerator.create_system_prompt()}
        
        ### User: Analyze this website titled "{title}".
        Provide a clear summary including any news or announcements.
        Use markdown formatting in your response.
        
        Content:
        {content}
        
        ### Assistant:"""

class MarkdownFormatter:
    """Handles markdown formatting operations"""
    @staticmethod
    def format_summary(url: str, title: str, summary: str, analysis_time: float) -> str:
        return f"""# Website Analysis Report

## 📊 Analysis Details
- **URL**: [{url}]({url})
- **Title**: {title}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Processing Time**: {analysis_time:.2f} seconds

## 📝 Summary
{summary}

---
*Generated using Ollama ({OllamaConfig.MODEL} model)*"""

    @staticmethod
    def format_error(error_message: str) -> str:
        return f"""# ❌ Error Report

An error occurred while analyzing the website:

```
{error_message}
```"""

class FileHandler:
    """Handles file operations"""
    @staticmethod
    def save_markdown(content: str) -> str:
        """Save markdown content to file and return filename"""
        filename = f"website_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename

class WebsiteAnalyzer:
    """Main class that orchestrates the website analysis process"""
    def __init__(self):
        self.scraper = WebScraper()
        self.ollama = OllamaService()

    def analyze(self, url: str) -> str:
        """Analyze website and return markdown formatted result"""
        if not self.ollama.check_availability():
            return MarkdownFormatter.format_error("Ollama is not running. Please start Ollama and try again.")
        
        try:
            start_time = datetime.now()
            
            # Fetch and parse website content
            response = self.scraper.fetch_page(url)
            soup = self.scraper.parse_html(response.content)
            title = self.scraper.extract_title(soup)
            content = self.scraper.clean_body_content(soup)
            
            # Generate and get summary
            prompt = PromptGenerator.create_user_prompt(title, content)
            summary = self.ollama.generate_summary(prompt)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Format output
            markdown_output = MarkdownFormatter.format_summary(
                url, title, summary, processing_time
            )
            
            # Save to file
            FileHandler.save_markdown(markdown_output)
            
            return markdown_output
            
        except Exception as e:
            return MarkdownFormatter.format_error(str(e))

def main():
    """Main function to run the website analyzer"""
    url = "https://en.wikipedia.org/wiki/World_War_II"
    print("\nAnalyzing website...\n")
    
    analyzer = WebsiteAnalyzer()
    result = analyzer.analyze(url)
    print(result)

if __name__ == "__main__":
    main()