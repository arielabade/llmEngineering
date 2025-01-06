import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import json
import openai  # Ensure correct library usage



# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Check the API key
if not api_key:
    print("No API key was found. Please fix it in your .env file.")
    exit(1)
elif not api_key.startswith("sk-"):
    print("API key found, but it doesn't start with 'sk-'. Please verify your key.")
    exit(1)
elif api_key.strip() != api_key:
    print("API key has leading or trailing spaces. Please fix it.")
    exit(1)
else:
    print("API key is valid.")

# Initialize OpenAI
openai.api_key = api_key

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
    return "Explain to me how vector databases storage for ai works."

# Function to generate answers
def generateAnswer(question):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    result = response.choices[0].message.content
    print(result)

# Example usage
question = user_prompt_for("example.com")
generateAnswer(question)




