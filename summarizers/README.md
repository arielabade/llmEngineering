# Summarizers Projects  

This document presents four **summarizer** projects designed to enhance information comprehension by summarizing content while maintaining its original meaning.  

## Key Integrations  
The summarizer projects leverage:  
- **Web Scraping**: Using libraries like `requests` and `BeautifulSoup`, the scripts extract relevant text from websites, removing unnecessary elements like images and scripts.  
- **API Integration (OpenAI and Ollama)**: Extracted content is sent to APIs for summarization. These models simplify information and, in some cases, explain concepts as if to a 5-year-old.  
- **Markdown Output**: Summaries are formatted in markdown for easy readability.  
- **Key Validation**: The scripts check the validity of API keys before making requests.  

---

## Projects  

### 1. [Simplifying for a 5-Year-Old](https://github.com/arielabade/llmEngineering/blob/main/summarizers/llmsAssistants/00summarizerOpenAI.py)  
- **Objective**: Summarize and explain complex information in an accessible way.  
- **Model Used**: OpenAI API.  
- **- **[Output](https://github.com/arielabade/llmEngineering/blob/main/summarizers/outputs/output00.md)****:  
  Example summary with data about a conflict in Ukraine:  
  - **38,000 soldiers** lost (according to Ukraine).  
  - Ukrainian troops advanced **18 miles** into Russian territory.  
  - **1,200 km²** of territory under Ukrainian control.  

---

### 2. [Scientific Personal Assistant](https://github.com/arielabade/llmEngineering/blob/main/summarizers/llmsAssistants/01personalAssistantTechConceptsOpenAI.py) and [Version with Ollama](https://github.com/arielabade/llmEngineering/blob/main/summarizers/llmsAssistants/01personalAssistantTechConceptsOllama.py)  
- **Objective**: Explain technical concepts in a scientific tone using questions like "how," "what," and "why."  
- **Models Used**: Ollama and OpenAI API.  
- **Example - Concept of Vector Databases**:  
  - **What is it?** A database optimized for storing and querying high-dimensional vectors.  
  - **How was it created?** Evolved from AI needs, utilizing indexing techniques like FAISS and HNSW.  
  - **Applications**: Similarity search, recommendation systems, and natural language processing.  

- **[Output](https://github.com/arielabade/llmEngineering/blob/main/summarizers/outputs/output01.md)**
---

### 3. [Explaining World War II](https://github.com/arielabade/llmEngineering/blob/main/summarizers/llmsAssistants/02summarizerOllama5YearOld.py)  
- **Objective**: Explain World War II to a 5-year-old.  
- **Model Used**: Ollama (Llama 3.2:1b).  
- **[Output](https://github.com/arielabade/llmEngineering/blob/main/summarizers/outputs/output02.md)**:  
  - **General Summary**: Wikipedia article divided into key events, including the European and Pacific theaters and the consequences of the war.  
  - **Limitations**: The model struggled to generate clear explanations due to its limited capabilities.  


---

### 4. [Vellum Brochure Generator](https://github.com/arielabade/llmEngineering/blob/main/summarizers/llmsAssistants/03vellumBrochureGenerator.py)  
- **Objective**: Create a promotional brochure for the **Vellum AI** platform.  
- **Model Used**: GPT-4o-mini.  
- **[Output](https://github.com/arielabade/llmEngineering/blob/main/summarizers/outputs/output03.md)**:  
  A successful commercial brochure highlighting:  
  - **Solutions**: Interactive workflows, experimentation, and AI monitoring.  
  - **Testimonials**: Satisfied clients like Drata, Woflow, and Redfin.  
  - **Call to Action**: Encouraging users to book demos and participate in surveys.  

---

This organization emphasizes the projects, highlighting their practical applications and relevant outputs.
