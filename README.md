# 🎓 Campus Knowledge Chatbot

An AI-powered chatbot that answers campus-related questions using Retrieval-Augmented Generation (RAG).

## 🚀 Features

* FastAPI backend
* Custom HTML/CSS/JS frontend
* Semantic search with embeddings
* Dark/Light mode UI
* Chat history navigation

## 🛠️ Tech Stack

* Python (FastAPI)
* ChromaDB
* Sentence Transformers
* HTML, CSS, JavaScript

## ▶️ How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Generate embeddings

```
python -m backend.ingestion.embed_store
```

### 3. Run backend

```
uvicorn api.server:app --reload
```

### 4. Open frontend

```
frontend/index.html
```

## ⚠️ Notes

* Add your API key in `.env`
* Do not upload `.env` file
* .env contains:
OPENROUTER_API_KEY=.......
