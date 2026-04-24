# 🎓 Budget-Aware Campus Knowledge Agent (RAG)

A Retrieval-Augmented Generation (RAG) chatbot that answers campus-related queries from PDFs with **source citations**.

## ✨ Features
- 📄 Ingest PDFs (rules, calendar, admissions, etc.)
- ✂️ Chunking + embeddings (Sentence Transformers)
- 🧠 Vector search (ChromaDB)
- 💬 LLM answers via OpenRouter
- 🔗 Source + page citations
- 🌐 Streamlit chat UI

## 🏗️ Architecture
User Query → Embed → Vector Search → Top-k Chunks → LLM → Final Answer (+ sources)

## 🛠 Tech Stack
- Python, Streamlit
- SentenceTransformers
- ChromaDB
- OpenRouter (LLMs)

## ▶️ Run Locally
```bash
cd CampusChatbot
venv\Scripts\activate
pip install -r requirements.txt

# (only when you add/update PDFs)
python -m backend.ingestion.embed_store

# start UI
streamlit run frontend/app.py

<h3>Project Strucuture</h3>
backend/
  ingestion/
  retrieval/
frontend/
data/
