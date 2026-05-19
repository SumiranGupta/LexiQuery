"""
LexiQuery Configuration Management
Centralized configuration via environment variables with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Fix SSL verification on corporate machines with SSL inspection
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

load_dotenv()

# ── Path Configuration ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
ANALYTICS_DIR = DATA_DIR / "analytics"

for _dir in [UPLOADS_DIR, VECTORSTORE_DIR, ANALYTICS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ── Embedding Configuration ─────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")  # kept for backward compat

# ── LLM Configuration ───────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))

# ── Chunking Configuration ──────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# ── Retrieval Configuration ─────────────────────────────────────────
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))

# ── FAISS Configuration ─────────────────────────────────────────────
FAISS_INDEX_PATH = VECTORSTORE_DIR / "faiss_index"

# ── Analytics Configuration ─────────────────────────────────────────
ANALYTICS_DB_PATH = ANALYTICS_DIR / "lexiquery.db"

# ── Supported File Types ────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".csv", ".docx", ".pptx", ".xlsx"}
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
