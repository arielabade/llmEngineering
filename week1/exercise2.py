import requests
from bs4 import BeautifulSoup
import json

# Configurações do Ollama
OLLAMA_API = "http://localhost:11434/api/generate"  # Changed to correct endpoint
MODEL = "llama3.2:1b"  # Changed to correct model name
HEADERS = {"Content-Type": "application/json"}

# Headers para scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# Classe Website para processar o conteúdo do site
class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        # Changed parser to 'html.parser' since lxml wasn't installed
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        
        if soup.body:
            for irrelevant in soup.body.find_all(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

# Definição do prompt do sistema
system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, focusing on relevant numeric data. Explain the relevant numeric data like people reading is a 5-year-old."

# Função para criar o prompt do usuário
def create_prompt(website):
    return f"""### System: {system_prompt}

### User: You are looking at a website titled {website.title}
The contents of this website are as follows; please provide a short summary of this website. If it includes news or announcements, then summarize these too.

{website.text}

### Assistant: """

# Função para se comunicar com o Ollama
def summarize(url):
    website = Website(url)
    prompt = create_prompt(website)
    
    # Criação do payload para a API do Ollama
    payload = {
        "model": MODEL, #easier
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Envio da requisição POST para a API do Ollama
        response = requests.post(OLLAMA_API, headers=HEADERS, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get("response", "No response content found.")
    except requests.exceptions.RequestException as e:
        print("Error communicating with Ollama:", e)
        return None

# Executar o resumo
if __name__ == "__main__":
    summary = summarize("https://edwarddonner.com")  # Changed to example.com for testing
    if summary:
        print(summary)
    else:
        print("Failed to generate summary.")