# LangChain RAG Project (FREE Local AI Version)

A fully offline Retrieval-Augmented Generation (RAG) system using:

- ChromaDB (Vector Database)
- Ollama (Local LLM - Llama3 / Mistral)
- HuggingFace Embeddings (Free)
- Markdown documents as knowledge base

No OpenAI API key required. Fully free and runs locally.

---

# Features

- Fully offline AI chatbot
- No API keys required
- Local LLM using Ollama
- Document-based question answering system
- Fast vector search using ChromaDB
- HuggingFace embeddings (free)

---

# Installation

## 1. Install dependencies

pip install -r requirements.txt

Then install required LangChain packages:

pip install -U langchain-chroma langchain-huggingface langchain-ollama

---

## 2. Install Ollama

Download from:
https://ollama.com

Then run:

ollama run llama3

(First time downloads ~4.7GB model)

---

# Project Structure

data/books/        → Documents (.md files)
chroma/            → Vector database (auto created)
create_database.py → Builds embeddings database
query_data.py      → Ask questions to AI

---

# Step 1: Create Database

python create_database.py

This will:
- Load documents
- Split into chunks
- Convert to embeddings
- Store in ChromaDB

---

# Step 2: Ask Questions

python query_data.py "Who is Alice?"

Example output:

Alice is the main character in Alice in Wonderland. She explores a fantasy world...

---

# How it works

1. Load documents
2. Split into chunks
3. Convert text into embeddings
4. Store in ChromaDB
5. Query → similarity search
6. Send context to Ollama LLM
7. Get final AI answer

---

# Tech Stack

- Python
- LangChain
- ChromaDB
- HuggingFace Transformers
- Ollama (LLaMA3)

---

# Notes

- First run is slow due to model download
- After that everything runs fast
- Works fully offline
- Ensure Ollama is running before querying

---

# Example Commands

python create_database.py
python query_data.py "Explain Alice story"

---

# Future Improvements

- Add Flask/Streamlit UI
- Add chat memory
- Add PDF support
- Deploy as web app

---

# Result

You now have a fully working offline ChatGPT-like system using your own documents.