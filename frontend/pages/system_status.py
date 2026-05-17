"""
System Status Page
Health checks, configuration overview, and administrative actions.
"""

import platform

import streamlit as st

from backend.utils.config import (
    EMBEDDING_MODEL,
    LLM_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K_RESULTS,
    GROQ_API_KEY,
    UPLOADS_DIR,
    VECTORSTORE_DIR,
)
from frontend.components.theme import COLORS


def render(vector_store, analytics_service, document_service):
    """Render the system status page."""
    st.markdown('<div class="page-header">⚙️ System Status</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Platform health and configuration</div>',
        unsafe_allow_html=True,
    )

    # ── Health Checks ───────────────────────────────────────────────
    st.markdown(f"""
        <p style="color: {COLORS['text_primary']}; font-weight: 600; font-size: 1.1rem;">
            🏥 Health Checks
        </p>
    """, unsafe_allow_html=True)

    checks = [
        ("FAISS Vector Store", vector_store.is_initialized,
         f"{vector_store.total_vectors} vectors"),
        ("Groq API Key", bool(GROQ_API_KEY),
         "Configured" if GROQ_API_KEY else "Missing — set GROQ_API_KEY"),
        ("Uploads Directory", UPLOADS_DIR.exists(), str(UPLOADS_DIR)),
        ("Vector Store Directory", VECTORSTORE_DIR.exists(), str(VECTORSTORE_DIR)),
    ]

    for name, ok, detail in checks:
        cls = "status-active" if ok else "status-processing"
        text = "Healthy" if ok else "Warning"
        st.markdown(f"""
            <div class="glass-card" style="padding: 12px 20px; display: flex;
                 align-items: center; justify-content: space-between;">
                <div>
                    <span style="color: {COLORS['text_primary']}; font-weight: 500;">
                        {name}
                    </span>
                    <span style="color: {COLORS['text_muted']}; font-size: 0.8rem;
                           margin-left: 12px;">
                        {detail}
                    </span>
                </div>
                <span class="status-badge {cls}">{text}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Configuration ───────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: {COLORS['text_primary']}; font-weight: 600;
                   margin-bottom: 12px;">
                    🧠 AI Configuration
                </p>
                <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem;
                     line-height: 2;">
                    <strong>LLM Model:</strong> {LLM_MODEL}<br>
                    <strong>Embedding Model:</strong> {EMBEDDING_MODEL}<br>
                    <strong>Chunk Size:</strong> {CHUNK_SIZE}<br>
                    <strong>Chunk Overlap:</strong> {CHUNK_OVERLAP}<br>
                    <strong>Top-K Results:</strong> {TOP_K_RESULTS}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: {COLORS['text_primary']}; font-weight: 600;
                   margin-bottom: 12px;">
                    💻 System Information
                </p>
                <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem;
                     line-height: 2;">
                    <strong>Python:</strong> {platform.python_version()}<br>
                    <strong>OS:</strong> {platform.system()} {platform.release()}<br>
                    <strong>Architecture:</strong> {platform.machine()}<br>
                    <strong>Vector DB:</strong> FAISS<br>
                    <strong>LLM Provider:</strong> Groq
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Admin Actions ───────────────────────────────────────────────
    st.markdown(f"""
        <p style="color: {COLORS['text_primary']}; font-weight: 600; font-size: 1.1rem;">
            🔧 Actions
        </p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🗑️ Reset Vector Store", use_container_width=True):
            vector_store.reset()
            analytics_service.clear_documents()
            st.success("Vector store and document records reset.")
            st.rerun()
    with c2:
        if st.button("🔄 Refresh Stats", use_container_width=True):
            st.rerun()
    with c3:
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat history cleared.")
