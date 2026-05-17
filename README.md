<div align="center">

# ⚡ LexiQuery

### AI Knowledge Platform

**Enterprise-grade RAG-powered document intelligence system**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)

</div>

---

## Overview

LexiQuery is a production-ready AI knowledge platform that lets you upload documents, build a searchable vector knowledge base, and ask natural-language questions with **citation-aware responses**. Built with an enterprise modular architecture, it features a modern dark-theme dashboard, real-time analytics, and is deployable on free-tier platforms.

### Key Features

| Feature | Description |
|---|---|
| **Multi-Document Upload** | Drag-and-drop PDFs, TXT, CSV, Markdown — processed and indexed automatically |
| **Advanced RAG Pipeline** | Semantic retrieval with top-k search, metadata-aware chunking, and context filtering |
| **Citation-Aware Responses** | Every answer shows source document, page number, and relevance score |
| **Enterprise Dashboard** | Analytics widgets, query history, system health, glassmorphism UI |
| **Lightweight AI Stack** | `all-MiniLM-L6-v2` embeddings (~80 MB) + Groq API — no GPU required |
| **Query Analytics** | Track documents, chunks, queries, latency, and top-referenced sources |
| **Production Ready** | Env vars, structured logging, error handling, caching, modular services |

---

## Architecture

```
LexiQuery/
├── app.py                          # Streamlit entry point
├── backend/
│   ├── ingestion/                  # Document loading & chunking
│   │   ├── loaders.py              # Multi-format document loaders
│   │   ├── chunker.py              # Recursive text splitting
│   │   └── pipeline.py             # End-to-end ingestion orchestration
│   ├── embeddings/
│   │   └── manager.py              # Lightweight embedding model (MiniLM-L6)
│   ├── vectorstores/
│   │   └── faiss_store.py          # FAISS index lifecycle management
│   ├── rag/
│   │   ├── retriever.py            # Semantic retrieval + citation extraction
│   │   └── chain.py                # LangChain RAG chain with Groq LLM
│   ├── services/
│   │   ├── analytics_service.py    # SQLite-based analytics tracking
│   │   ├── document_service.py     # File management
│   │   └── query_service.py        # Query orchestration
│   └── utils/
│       ├── config.py               # Centralized env-var configuration
│       └── logger.py               # Structured logging
├── frontend/
│   ├── components/                 # Reusable UI components
│   │   ├── theme.py                # Enterprise dark theme CSS
│   │   ├── sidebar.py              # Navigation sidebar
│   │   ├── chat.py                 # Chat interface with citations
│   │   ├── upload.py               # Upload zone component
│   │   ├── metrics.py              # Glassmorphism metric cards
│   │   └── analytics.py            # Plotly chart components
│   └── pages/                      # Application pages
│       ├── dashboard.py            # Analytics dashboard
│       ├── upload_center.py        # Document management
│       ├── ai_assistant.py         # AI chat interface
│       ├── query_history.py        # Query log browser
│       └── system_status.py        # Health checks & config
├── data/
│   ├── uploads/                    # Uploaded documents
│   ├── vectorstore/                # FAISS index files
│   └── analytics/                  # SQLite analytics database
├── .env.example                    # Environment variable template
├── requirements.txt                # Python dependencies
├── Procfile                        # Render / Heroku deployment
├── render.yaml                     # Render deploy config
└── .streamlit/config.toml          # Streamlit theme configuration
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/LexiQuery.git
cd LexiQuery
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure

```bash
copy .env.example .env
# Edit .env and add your Groq API key
```

Get a free Groq API key at [console.groq.com](https://console.groq.com/).

### 3. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Frontend** | Streamlit + Custom CSS | Rapid enterprise UI with glassmorphism theme |
| **LLM** | DeepSeek R1 via Groq | Free, fast inference — no local GPU needed |
| **Embeddings** | all-MiniLM-L6-v2 | Lightweight (~80 MB), CPU-friendly, high quality |
| **Vector Store** | FAISS | Fast similarity search, zero infrastructure |
| **Framework** | LangChain | Production RAG pipelines with modular chains |
| **Analytics** | SQLite + Plotly | Zero-dependency tracking with rich visualizations |
| **Document Loading** | PDFPlumber, LangChain Loaders | Multi-format support (PDF, TXT, CSV, MD) |

---

## Deployment

### Streamlit Cloud

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as entrypoint
4. Add `GROQ_API_KEY` in the Secrets section

### Render

1. Push your repo to GitHub
2. Create a new Web Service on [render.com](https://render.com)
3. Connect your repo — `render.yaml` auto-configures the build
4. Add `GROQ_API_KEY` in Environment Variables

---

## Configuration

All settings are configurable via environment variables (see [.env.example](.env.example)):

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | Groq API key (required) |
| `LLM_MODEL` | `deepseek-r1-distill-llama-70b` | Groq model name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `CHUNK_SIZE` | `1000` | Text chunk size in characters |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `TOP_K_RESULTS` | `5` | Number of retrieved chunks per query |

---

## Future Roadmap

- [ ] DOCX and HTML document support
- [ ] Reranking with cross-encoders
- [ ] Hybrid retrieval (BM25 + semantic)
- [ ] Multi-user with authentication
- [ ] API endpoints (FastAPI)
- [ ] Webhook / database source ingestion
- [ ] Export chat sessions

---

## License

MIT

