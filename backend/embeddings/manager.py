"""
Embedding Model Manager
Uses FastEmbed (ONNX, no PyTorch) when available — ideal for low-memory cloud deployment.
Falls back to HuggingFaceEmbeddings (sentence-transformers) for local development.
"""

from functools import lru_cache

from backend.utils.config import EMBEDDING_MODEL, EMBEDDING_DEVICE
from backend.utils.logger import get_logger

logger = get_logger("embeddings.manager")


@lru_cache(maxsize=1)
def get_embedding_model():
    """Return a cached embedding model.
    Prefers FastEmbed (ONNX, ~100 MB, no PyTorch) on Render/production.
    Falls back to HuggingFaceEmbeddings (sentence-transformers) for local dev.
    """
    # ── Try FastEmbed first (ONNX, low-memory, no PyTorch) ──────────
    try:
        from langchain_community.embeddings import FastEmbedEmbeddings
        logger.info(f"Initializing embedding model: {EMBEDDING_MODEL} (ONNX/FastEmbed)")
        embeddings = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
        logger.info("Embedding model ready (FastEmbed)")
        return embeddings
    except ImportError:
        pass

    # ── Fall back to HuggingFaceEmbeddings (sentence-transformers) ───
    from langchain_huggingface import HuggingFaceEmbeddings
    logger.info(f"Initializing embedding model: {EMBEDDING_MODEL} (HuggingFace fallback)")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )
    logger.info("Embedding model ready (HuggingFace)")
    return embeddings

