"""
LexiQuery — AI Knowledge Platform
Enterprise-grade RAG-based document intelligence system.

Run:  streamlit run app.py
"""

import streamlit as st

# ── Page config must be the very first Streamlit command ────────────
st.set_page_config(
    page_title="LexiQuery — AI Knowledge Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from frontend.components.theme import apply_theme
from frontend.components.sidebar import render_sidebar
from frontend.pages import (
    dashboard,
    upload_center,
    ai_assistant,
    query_history,
    system_status,
)
from backend.vectorstores.faiss_store import FAISSStore
from backend.rag.retriever import Retriever
from backend.rag.chain import RAGChain
from backend.ingestion.pipeline import IngestionPipeline
from backend.services.analytics_service import AnalyticsService
from backend.services.document_service import DocumentService
from backend.services.query_service import QueryService

# ── Apply theme ─────────────────────────────────────────────────────
apply_theme()


# ── Initialize services (cached once across sessions) ──────────────
@st.cache_resource
def _init_services():
    analytics = AnalyticsService()
    vector_store = FAISSStore()
    retriever = Retriever(vector_store)
    rag_chain = RAGChain(retriever)
    ingestion = IngestionPipeline(vector_store, analytics)
    query_svc = QueryService(rag_chain, analytics)
    doc_svc = DocumentService()

    return {
        "analytics": analytics,
        "vector_store": vector_store,
        "ingestion": ingestion,
        "query_service": query_svc,
        "document_service": doc_svc,
    }


svc = _init_services()

# ── Sidebar navigation & page routing ──────────────────────────────
page = render_sidebar()

if page == "Dashboard":
    dashboard.render(svc["analytics"])

elif page == "Upload Center":
    upload_center.render(
        svc["ingestion"],
        svc["document_service"],
        svc["analytics"],
    )

elif page == "AI Assistant":
    ai_assistant.render(svc["query_service"], svc["vector_store"])

elif page == "Query History":
    query_history.render(svc["analytics"])

elif page == "System Status":
    system_status.render(
        svc["vector_store"],
        svc["analytics"],
        svc["document_service"],
    )
