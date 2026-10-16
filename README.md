# Langchain Learning

My LangChain learning path, from calling chat models and embeddings to complete multi-document RAG systems and a CSV retrieval agent.

**Tech:** Python, LangChain, ChromaDB, Hugging Face, Groq

## What's inside

- `langchain-models/`: chat models, LLMs and embedding models
- `multi-doc-rag/`: RAG over PDF/DOCX/PPTX with an API
- `multi-doc-rag-v2/`: refactored ingestion with a loader router
- `csv-retrieval-agent/`: agent that answers questions about CSV data

## Run it

```bash
cd <project-folder>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

API keys are read from environment variables. Copy `.env.example` to `.env` and fill in your own keys.

---
By [Muhammad Ali](https://muhammad773-bit.github.io), BS Artificial Intelligence, SMIU Karachi.
