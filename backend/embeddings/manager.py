"""
Embedding Model Manager
Provides cached, lightweight embedding models suitable for low-memory environments.
Default: all-MiniLM-L6-v2 via FastEmbed (ONNX) — ~100 MB, no PyTorch required.
"""

from functools import lru_cache

from langchain_community.embeddings import FastEmbedEmbeddings

from backend.utils.config import EMBEDDING_MODEL
from backend.utils.logger import get_logger

logger = get_logger("embeddings.manager")


@lru_cache(maxsize=1)
def get_embedding_model() -> FastEmbedEmbeddings:
    """Return a cached FastEmbed (ONNX) embedding model instance."""
    logger.info(f"Initializing embedding model: {EMBEDDING_MODEL} (ONNX/FastEmbed)")
    embeddings = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
    logger.info("Embedding model ready")
    return embeddings
