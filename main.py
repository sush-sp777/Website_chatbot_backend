from fastapi import FastAPI
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import re

app = FastAPI()

class Query(BaseModel):
    user_query: str

def load_cleaned_text():
    with open("visionq_cleaned.txt", "r", encoding="utf-8") as f:
        return f.read()

def create_vectorstore():
    text = load_cleaned_text()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.create_documents([text])
    embeddings = OllamaEmbeddings(model="mistral")  # optimized quantized model
    return FAISS.from_documents(docs, embeddings)

vectorstore = create_vectorstore()
retriever = vectorstore.as_retriever(k=3)
llm = OllamaLLM(model="mistral")  # fast and accurate

prompt = ChatPromptTemplate.from_template(
    """
Use only the provided context to answer the user's question.
Keep the response concise and accurate.
Do not include generic summaries or unrelated information.

Context:
{context}

Question:
{input}
"""
)

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

@app.post("/chat")
async def chat(query: Query):
    result = retrieval_chain.invoke({"input": query.user_query})
    raw_answer = result.get("answer", "Sorry, I couldn't find the answer.")

    # Clean any unwanted prefix and ensure clarity
    cleaned_answer = re.sub(r"(?i)(System:|Context:|Answer:|Response:|Human:|\n)+", " ", raw_answer)
    cleaned_answer = re.sub(r"\s+", " ", cleaned_answer).strip()

    # Prevent vague, repeated, or misleading content
    banned_phrases = [
        "here are some questions",
        "please provide answers",
        "according to available data",
        "based on the context provided",
        "our company",
        "we can assure you",
        "contact their customer service",
        "visit their official website",
        "latest tech updates, offers"
    ]
    if any(phrase in cleaned_answer.lower() for phrase in banned_phrases):
        return {"answer": "Sorry, I couldn't find a direct answer. Try rephrasing your question."}

    # Apply brand tone changes
    brand_tone_replacements = {
        r"\b[Tt]he company\b": "our company VisionQ Technology",
        r"\b[Tt]he VisionQ Technology team\b": "our VisionQ Technology team",
        r"\b[Mm]essage them\b": "message our team",
        r"\b[Cc]ontact them\b": "contact our team",
        r"\b[Tt]he team\b": "our team",
        r"\b[Vv]isionQ Technology\b": "our company VisionQ Technology"
    }

    for pattern, replacement in brand_tone_replacements.items():
        cleaned_answer = re.sub(pattern, replacement, cleaned_answer)

    return {"answer": cleaned_answer}
