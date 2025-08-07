# 🧠 Website Chatbot (RAG using Mistral + FastAPI + LangChain)

This project is an intelligent chatbot built using **FastAPI** and **LangChain**, powered by **Mistral via Ollama**.  
It performs Retrieval-Augmented Generation (RAG) by scraping and embedding data from the website using **FAISS**, and serves context-specific responses via a REST API.

---

## 🔧 Requirements

- Python 3.10+
- Ollama (for running Mistral locally)

Install Python dependencies:

```bash
pip install -r requirements.txt

🧩 Steps to Run
1️⃣ Scrape website content
Extract data using:

python scrape.py

2️⃣ Clean the scraped text
Format and filter the content:

python clean.py

3️⃣ Install Ollama
Download and install Ollama from:
👉 https://ollama.com/download

4️⃣ Pull the Mistral model
Once Ollama is installed, open your terminal and run:

ollama pull mistral

Wait until you see a success message confirming the model is ready.

5️⃣ Start the FastAPI server

🚀 How to Use (via Swagger UI)
Once the server is running, open your browser and go to:
👉 http://127.0.0.1:8000/docs

Under the /chat POST endpoint, click "Try it out"

Click Execute to see the chatbot's response powered by Mistral + LangChain

📁 Project Structure (optional to include)

chatbot/
├── main.py           # FastAPI app
├── scrape.py         # Web scraping logic
├── clean.py          # Text cleaning and formatting
├── requirements.txt  # Python dependencies
