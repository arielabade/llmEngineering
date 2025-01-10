
## Code


from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json
import openai

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Corrected the GPT model name
gpt_model = "gpt-4o-mini"  # or any other valid OpenAI model

if openai_api_key:
    print(f"OpenAI API Key exists and begins with {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    exit(1)  # Exit if no API key is available

# Ollama API configuration
OLLAMA_API = "http://localhost:11434/api/generate"  # Corrected endpoint
MODEL = "llama3.2"  # Corrected model name
OLLAMA_HEADERS = {"Content-Type": "application/json"}

# System messages
gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

ollama_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initial messages
gpt_messages = ["Hi there"]
ollama_messages = ["Hi"]

def check_ollama():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/version")
        if response.status_code == 200:
            return True
        else:
            print(f"✗ Error connecting to Ollama: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to Ollama. Make sure Ollama is installed and running.")
        return False
    except Exception as e:
        print(f"✗ Error connecting to Ollama: {e}")
        return False

def call_gpt(gpt_messages, ollama_messages):
    """
    Function to call the GPT API
    """
    messages = [{"role": "system", "content": gpt_system}]
    
    for gpt, ollama in zip(gpt_messages, ollama_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": ollama})
    
    if len(ollama_messages) > 0:
        messages.append({"role": "user", "content": ollama_messages[-1]})
    
    try:
        completion = client.chat.completions.create(
            model=gpt_model,
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling GPT: {e}")
        return None

def call_ollama(last_gpt_response):
    """
    Function to call the Ollama API with the last GPT response as input.
    """
    if not check_ollama():
        return None
    
    # Build the prompt for Ollama
    prompt = f"### System: {ollama_system}\n\n### User: {last_gpt_response}\n\n### Assistant:"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "max_tokens": 500
        }
    }
    
    try:
        response = requests.post(
            OLLAMA_API,
            json=payload,
            headers=OLLAMA_HEADERS
        )
        response.raise_for_status()
        result = response.json()
        
        if "response" in result and result["response"].strip():
            return result["response"]
        else:
            print("Unexpected format or empty response from Ollama API:", result)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return None


def chat_loop():
    """
    Function for the continuous chat loop between GPT and Ollama
    """
    print("Starting continuous chat... (5 interactions)")
    
    # Displaying initial messages in Markdown
    print(f"```markdown\n**GPT:**\n{gpt_messages[0]}\n```")
    print(f"```markdown\n**Ollama:**\n{ollama_messages[0]}\n```")
    
    for i in range(5):
        # Call GPT
        gpt_next = call_gpt(gpt_messages, ollama_messages)
        if gpt_next:
            print(f"```markdown\n**GPT:**\n{gpt_next}\n```")
            gpt_messages.append(gpt_next)
        
        # Call Ollama
        ollama_next = call_ollama(gpt_next)
        if ollama_next:
            print(f"```markdown\n**Ollama:**\n{ollama_next}\n```")


if __name__ == "__main__":
    chat_loop()
