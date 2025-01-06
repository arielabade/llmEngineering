import os
import requests
from dotenv import load_dotenv
import json

# Constants for Ollama API
OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2:1b"  # Updated model name

# Load environment variables
load_dotenv(override=True)

# Check if Ollama is properly configured (no API key needed for local Ollama)
def check_ollama():
    try:
        response = requests.get(f"{OLLAMA_API.replace('/generate', '')}/models")
        if response.status_code == 200:
            print("Ollama is running and accessible.")
        else:
            print(f"Error connecting to Ollama: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        exit(1)

check_ollama()

# Headers for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# System prompt definition
system_prompt = (
    "You are an assistant that explains technology concepts, including code, math, debugging, and AI. "
    "Focus on fundamentals and answer in a structured way: what it is, how it was created, and its use."
)

# Function to generate user prompt
def user_prompt_for(website):   
    return "Explain to me how vector databases storage for AI works."

# Function to generate answers with Ollama
def generate_ollama_answer(prompt):
    payload = {
        "model": MODEL,  # Updated to use the corrected model name
        "prompt": f"{system_prompt}\nUser: {prompt}\nAssistant:",
        "stream": False  # Added stream parameter
    }
    try:
        response = requests.post(OLLAMA_API, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json().get("response", "No response generated.")
        print("\nResponse from Ollama:")
        print(result)
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None

# Example usage
question = user_prompt_for("example.com")
ollama_answer = generate_ollama_answer(question)
