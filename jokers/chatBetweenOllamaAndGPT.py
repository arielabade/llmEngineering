from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
import json
import openai

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Corrected GPT model name
gpt_model = "gpt-4o-mini"  # or another valid OpenAI model

if openai_api_key:
    print(f"OpenAI API Key exists and begins with {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    exit(1)  # Exit if no API key is set

# Ollama API configuration
OLLAMA_API = "http://localhost:11434/api/generate"  # Corrected endpoint
MODEL = "llama2"  # Corrected model name

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

def call_gpt(gpt_messages, ollama_messages):
    """
    Function to call the GPT API
    """
    messages = [{"role": "system", "content": gpt_system}]
    
    # Corrected the message loop
    for gpt, ollama in zip(gpt_messages, ollama_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": ollama})
    
    # Adding last message if necessary
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

def call_ollama(gpt_messages, ollama_messages, model="llama2"):
    """
    Function to call the Ollama API
    """
    messages = [{"role": "system", "content": ollama_system}]
    
    # Combining alternating messages
    for gpt, ollama in zip(gpt_messages, ollama_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": ollama})
    
    # Adding the last user message if there is one
    if len(gpt_messages) > len(ollama_messages):
        messages.append({"role": "user", "content": gpt_messages[-1]})
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "max_tokens": 500
        }
    }
    
    try:
        response = requests.post(
            OLLAMA_API,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling the Ollama API: {e}")
        return None

def interactive_chat():
    """
    Function for interactive chat
    """
    print("Starting chat... (type 'exit' to end)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        gpt_messages.append(user_input)
        
        # Call GPT
        gpt_response = call_gpt(gpt_messages, ollama_messages)
        if gpt_response:
            print(f"GPT: {gpt_response}")
            ollama_messages.append(gpt_response)
            
            # Call Ollama
            ollama_response = call_ollama(gpt_messages, ollama_messages)
            if ollama_response:
                print(f"Ollama: {ollama_response}")
                gpt_messages.append(ollama_response)

if __name__ == "__main__":
    interactive_chat()
