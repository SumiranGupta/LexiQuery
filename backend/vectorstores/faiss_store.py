"""
FAISS Vector Store Manager
Handles creation, persistence, incremental updates, and similarity search
for the FAISS vector index.
"""

import shutil
from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from backend.embeddings.manager import get_embedding_model
from backend.utils.config import FAISS_INDEX_PATH, TOP_K_RESULTS
from backend.utils.logger import get_logger

logger = get_logger("vectorstores.faiss")


class FAISSStore:
    """Manages the full lifecycle of a FAISS vector index."""

    def __init__(self, index_path: Path = FAISS_INDEX_PATH):
        self.index_path = index_path
        self.embeddings = get_embedding_model()
        self._db: Optional[FAISS] = None
        self._load_existing()

    # ── Initialization ──────────────────────────────────────────────

    def _load_existing(self):
        """Attempt to load a previously persisted index."""
        index_file = self.index_path / "index.faiss"
        if index_file.exists():
            try:
                self._db = FAISS.load_local(
                    str(self.index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                logger.info(f"Loaded existing FAISS index — {self.total_vectors} vectors")
            except Exception as e:
                logger.warning(f"Could not load existing index: {e}. Starting fresh.")
                self._db = None
        else:
            logger.info("No existing FAISS index found. Will create on first ingestion.")

    # ── Properties ──────────────────────────────────────────────────

    @property
    def is_initialized(self) -> bool:
        return self._db is not None

    @property
    def total_vectors(self) -> int:
        return self._db.index.ntotal if self._db else 0

    # ── Write Operations ────────────────────────────────────────────

    def add_documents(self, documents: List[Document]):
        """Add documents to the index, creating it if needed."""
        if not documents:
            return

        if self._db is None:
            self._db = FAISS.from_documents(documents, self.embeddings)
            logger.info(f"Created new FAISS index with {len(documents)} vectors")
        else:
            self._db.add_documents(documents)
            logger.info(f"Added {len(documents)} vectors to existing index")

        self._save()

    def reset(self):
        """Delete and reinitialize the vector store."""
        # Release the Python FAISS object FIRST so handles are freed before we
        # try to delete the files (critical on Windows / OneDrive).
        self._db = None
        if self.index_path.exists():
            try:
                shutil.rmtree(self.index_path)
            except Exception as e:
                logger.warning(f"shutil.rmtree failed ({e}), falling back to per-file deletion")
                for f in self.index_path.glob("*"):
                    try:
                        f.unlink(missing_ok=True)
                    except Exception:
                        pass
                try:
                    self.index_path.rmdir()
                except Exception:
                    pass
        logger.info("FAISS index reset")

    # ── Read Operations ─────────────────────────────────────────────

    def similarity_search(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """Retrieve top-k similar documents with similarity scores."""
        if not self.is_initialized:
            logger.warning("FAISS index not initialized — no documents to search.")
            return []

        results = self._db.similarity_search_with_score(query, k=k)

        docs = []
        for doc, score in results:
            doc.metadata["similarity_score"] = round(float(score), 4)
            docs.append(doc)

        logger.info(f"Retrieved {len(docs)} results for query (first 80 chars): {query[:80]}")
        return docs

    # ── Persistence ─────────────────────────────────────────────────

    def _save(self):
        """Write the current index to disk."""
        if self._db:
            self.index_path.mkdir(parents=True, exist_ok=True)
            self._db.save_local(str(self.index_path))
            logger.info(f"FAISS index saved — {self.total_vectors} vectors")
