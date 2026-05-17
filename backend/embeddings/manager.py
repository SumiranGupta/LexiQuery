"""
Embedding Model Manager
Provides cached, lightweight embedding models suitable for low-memory environments.
Default: all-MiniLM-L6-v2 (~80 MB) — runs on CPU with minimal resources.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from backend.utils.config import EMBEDDING_MODEL, EMBEDDING_DEVICE
from backend.utils.logger import get_logger

logger = get_logger("embeddings.manager")


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """Return a cached embedding model instance (loaded once, reused)."""
    logger.info(f"Initializing embedding model: {EMBEDDING_MODEL} on {EMBEDDING_DEVICE}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )

    logger.info("Embedding model ready")
    return embeddings
