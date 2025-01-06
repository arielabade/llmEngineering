import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI


# Load environment variables
class Config:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = 'gpt-4o-mini'
        self.openai = OpenAI() 

    def validate_api_key(self):
        if self.api_key and self.api_key.startswith('sk-proj-') and len(self.api_key) > 10:
            print("API key looks good so far")
        else:
            print("There might be a problem with your API key. Please visit the troubleshooting notebook!")


# Class to handle API communication with OpenAI
class OpenAICommunicator:
    def __init__(self, openai_instance, model):
        self.openai = openai_instance
        self.model = model

    def get_response(self, system_prompt, user_prompt):
        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            response_content = response.choices[0].message.content
            if not response_content:
                print("Error: Empty response from OpenAI")
                return "{}"  # Return empty JSON structure
            return response_content
        except Exception as e:
            print(f"Error fetching response from OpenAI: {e}")
            return "{}"  # Return empty JSON structure in case of error


# Class to represent a Website and extract its content
class Website:
    def __init__(self, url):
        self.url = url
        self.body = self._fetch_website_content()
        self.title, self.text, self.links = self._parse_content()

    def _fetch_website_content(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)
        return response.content

    def _parse_content(self):
        soup = BeautifulSoup(self.body, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        text = ""
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        return title, text, links

    def get_contents(self):
        return f"## Webpage Title:\n{self.title}\n\n## Webpage Contents:\n{self.text}\n\n"


# Class for Brochure creation logic
class BrochureCreator:
    def __init__(self, company_name, url, openai_communicator):
        self.company_name = company_name
        self.url = url
        self.openai_communicator = openai_communicator

    def _get_links_user_prompt(self, website):
        user_prompt = f"Here is the list of links on the website of {website.url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, or email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(website.links)
        return user_prompt

    def _get_links(self, website):
        link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
        link_system_prompt += "You should respond in JSON format as shown in the example below:\n"
        link_system_prompt += """
        {
            "links": [
                {"type": "about page", "url": "https://full.url/goes/here/about"},
                {"type": "careers page", "url": "https://another.full.url/careers"}
            ]
        }
        """
        user_prompt = self._get_links_user_prompt(website)
        response_content = self.openai_communicator.get_response(link_system_prompt, user_prompt)
        try:
            return json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {"links": []}  # Return empty links in case of error

    def _get_all_details(self):
        website = Website(self.url)
        result = f"## Landing page:\n{website.get_contents()}"
        links = self._get_links(website)
        print("Found links:", links)
        for link in links["links"]:
            result += f"\n\n## {link['type']}:\n"
            result += Website(link["url"]).get_contents()
        return result

    def _get_brochure_user_prompt(self):
        user_prompt = f"You are looking at a company called: {self.company_name}\n"
        user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        user_prompt += self._get_all_details()
        user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
        return user_prompt

    def create_brochure(self):
        system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors, and recruits. Respond in markdown.\
Include details of company culture, customers, and careers/jobs if you have the information."
        user_prompt = self._get_brochure_user_prompt()
        markdown_response = self.openai_communicator.get_response(system_prompt, user_prompt)
        return markdown_response


# Main Function to Execute Brochure Creation
def generate_brochure():
    config = Config()
    config.validate_api_key()
    openai_communicator = OpenAICommunicator(config.openai, config.model)
    brochure_creator = BrochureCreator("vellum", "https://www.vellum.ai", openai_communicator)
    brochure_content = brochure_creator.create_brochure()
    print("Generated Brochure in Markdown:\n")
    print(brochure_content)


generate_brochure()
