"""
Retrieval Module
Handles document retrieval with metadata enrichment and citation extraction.
Designed to be reranking-ready and hybrid-retrieval-ready.
"""

from typing import List, Dict, Any

from langchain_core.documents import Document

from backend.vectorstores.faiss_store import FAISSStore
from backend.utils.config import TOP_K_RESULTS
from backend.utils.logger import get_logger

logger = get_logger("rag.retriever")


class Retriever:
    """Retrieves relevant document chunks with citation metadata."""

    def __init__(self, vector_store: FAISSStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = TOP_K_RESULTS) -> List[Document]:
        """Retrieve top-k relevant chunks for a query."""
        if not self.vector_store.is_initialized:
            return []
        return self.vector_store.similarity_search(query, k=top_k)

    # ── Context Formatting ──────────────────────────────────────────

    @staticmethod
    def format_context(documents: List[Document]) -> str:
        """Format retrieved documents into a numbered context string."""
        if not documents:
            return ""

        parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source_file", "Unknown")
            page = doc.metadata.get("page", "?")
            parts.append(f"[Source {i}: {source}, Page {page}]\n{doc.page_content}")

        return "\n\n---\n\n".join(parts)

    # ── Citation Extraction ─────────────────────────────────────────

    @staticmethod
    def extract_citations(documents: List[Document]) -> List[Dict[str, Any]]:
        """Extract deduplicated citation metadata from retrieved documents."""
        citations = []
        seen = set()

        for doc in documents:
            source = doc.metadata.get("source_file", "Unknown")
            page = doc.metadata.get("page", "?")
            score = doc.metadata.get("similarity_score", 0)
            key = (source, page)

            if key not in seen:
                seen.add(key)
                citations.append({
                    "source": source,
                    "page": page,
                    "score": score,
                    "chunk_preview": doc.page_content[:150] + "...",
                })

        return citations
