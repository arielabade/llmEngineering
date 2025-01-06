import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Constants for Ollama API
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"  # Change this to your installed model name

def check_ollama():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/version")
        if response.status_code == 200:
            print("✓ Ollama is running and accessible")
            return True
        else:
            print(f"✗ Error connecting to Ollama: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to Ollama. Make sure Ollama is installed and running.")
        print("  Installation instructions:")
        print("  - Mac/Linux: curl https://ollama.ai/install.sh | sh")
        print("  - Windows: Download from https://ollama.ai")
        return False
    except Exception as e:
        print(f"✗ Error connecting to Ollama: {e}")
        return False

def generate_answer(question, system_prompt):
    """Generate answer using Ollama"""
    if not check_ollama():
        return None
        
    payload = {
        "model": MODEL,
        "prompt": f"### System: {system_prompt}\n\n### User: {question}\n\n### Assistant:",
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API, headers=OLLAMA_HEADERS, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response generated.")
    except requests.exceptions.RequestException as e:
        print(f"Error generating response: {e}")
        return None

def main():
    # System prompt definition
    system_prompt = """You are an assistant that explains technology concepts, including code, math, debugging, and AI. 
    Focus on fundamentals and answer in a structured way using markdown formatting:
    1. What it is
    2. How it was created
    3. Its practical use
    
    Format your response in clear markdown with headers, lists, and code examples where appropriate."""
    
    # Example question about vector databases
    question = "Explain to me how vector databases storage for AI works."
    
    print("\nGenerating response...\n")
    response = generate_answer(question, system_prompt)
    
    if response:
        # Create markdown output
        output = f"""# Technology Concept Explanation
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Query
{question}

## Response
{response}

---
*Generated using Ollama with {MODEL} model*
"""
        
        # Print to console and save to file
        print(output)
        
        # Save to markdown file
        filename = "tech_explanation.md"
        with open(filename, "w") as f:
            f.write(output)
        print(f"\nResponse saved to {filename}")

if __name__ == "__main__":
    main()