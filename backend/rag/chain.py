"""
RAG Chain
Orchestrates retrieval → context building → LLM generation → citation attachment.
"""

import ssl
import time
from typing import Dict, Any

import httpx
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from backend.rag.retriever import Retriever
from backend.utils.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from backend.utils.logger import get_logger


def _make_http_client() -> httpx.Client:
    """Build an httpx client that trusts the Windows/system certificate store.
    Falls back to default (certifi) if truststore is not installed."""
    try:
        import truststore
        ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        return httpx.Client(verify=ctx)
    except Exception:
        return httpx.Client()

logger = get_logger("rag.chain")

SYSTEM_PROMPT = """You are LexiQuery, an advanced AI knowledge assistant. \
Answer the user's question accurately based ONLY on the provided context.

Rules:
1. Use only information present in the context.
2. If the context lacks sufficient information, state that clearly.
3. Reference specific sources when possible (e.g., "According to [Source 1]...").
4. Be concise, professional, and well-structured.
5. Use bullet points or numbered lists for clarity when appropriate.

Context:
{context}

Question: {question}

Answer:"""


def _get_llm() -> ChatGroq:
    """Initialize the Groq LLM with a corporate-SSL-aware httpx client."""
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        api_key=GROQ_API_KEY or None,
        http_client=_make_http_client(),
    )


class RAGChain:
    """Full RAG pipeline: retrieve → generate → cite."""

    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.llm = _get_llm()
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        self.chain = self.prompt | self.llm

    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """Execute a full RAG query and return response with citations."""
        start = time.time()

        # ── Retrieve ────────────────────────────────────────────────
        t0 = time.time()
        documents = self.retriever.retrieve(question, top_k=top_k)
        retrieval_ms = (time.time() - t0) * 1000

        if not documents:
            return {
                "answer": (
                    "No documents found in the knowledge base. "
                    "Please upload documents first via the Upload Center."
                ),
                "citations": [],
                "retrieval_latency_ms": round(retrieval_ms, 1),
                "total_latency_ms": round((time.time() - start) * 1000, 1),
                "chunks_retrieved": 0,
            }

        # ── Generate ────────────────────────────────────────────────
        context = self.retriever.format_context(documents)
        citations = self.retriever.extract_citations(documents)

        response = self.chain.invoke({"question": question, "context": context})
        answer = response.content if hasattr(response, "content") else str(response)

        # Strip <think>…</think> blocks from DeepSeek reasoning models
        if "<think>" in answer:
            parts = answer.split("</think>")
            answer = parts[-1].strip() if len(parts) > 1 else answer

        total_ms = (time.time() - start) * 1000
        logger.info(f"Query done in {total_ms:.0f}ms (retrieval: {retrieval_ms:.0f}ms)")

        return {
            "answer": answer,
            "citations": citations,
            "retrieval_latency_ms": round(retrieval_ms, 1),
            "total_latency_ms": round(total_ms, 1),
            "chunks_retrieved": len(documents),
        }
