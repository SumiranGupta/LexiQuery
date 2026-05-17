"""
Query Service
Orchestrates the query pipeline and records analytics.
"""

from typing import Dict, Any

from backend.rag.chain import RAGChain
from backend.services.analytics_service import AnalyticsService
from backend.utils.logger import get_logger

logger = get_logger("services.query")


class QueryService:
    """Processes user queries through the RAG pipeline with analytics tracking."""

    def __init__(self, rag_chain: RAGChain, analytics: AnalyticsService):
        self.rag_chain = rag_chain
        self.analytics = analytics

    def ask(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """Process a user query and record analytics."""
        logger.info(f"Processing query: {question[:100]}...")

        result = self.rag_chain.query(question, top_k=top_k)

        self.analytics.record_query({
            "query": question,
            "answer": result["answer"],
            "citations": result["citations"],
            "chunks_retrieved": result["chunks_retrieved"],
            "retrieval_latency_ms": result["retrieval_latency_ms"],
            "total_latency_ms": result["total_latency_ms"],
        })

        return result
