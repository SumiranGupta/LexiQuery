"""
AI Assistant Page
Chat interface with citation-aware responses and retrieval metrics.
"""

import streamlit as st

from frontend.components.chat import render_chat_message, render_chat_input
from frontend.components.theme import COLORS


def render(query_service, vector_store):
    """Render the AI Assistant chat page."""
    st.markdown('<div class="page-header">🤖 AI Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Ask questions about your uploaded documents</div>',
        unsafe_allow_html=True,
    )

    # ── Status ──────────────────────────────────────────────────────
    if vector_store.is_initialized:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                <span class="status-badge status-active">● Ready</span>
                <span style="color: {COLORS['text_muted']}; font-size: 0.8rem;">
                    {vector_store.total_vectors} vectors indexed
                </span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(
            "⚠️ No documents indexed yet. "
            "Please upload documents in the Upload Center first."
        )

    # ── Session State ───────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ── Settings ────────────────────────────────────────────────────
    with st.expander("⚙️ Retrieval Settings"):
        c1, c2 = st.columns(2)
        with c1:
            top_k = st.slider("Top-K Results", min_value=1, max_value=15, value=5)
        with c2:
            show_citations = st.checkbox("Show Citations", value=True)

    # ── Chat History ────────────────────────────────────────────────
    for msg in st.session_state.messages:
        render_chat_message(
            msg["role"],
            msg["content"],
            msg.get("citations") if show_citations else None,
        )

    # ── Input ───────────────────────────────────────────────────────
    user_input = render_chat_input()

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_chat_message("user", user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = query_service.ask(user_input, top_k=top_k)

            st.markdown(result["answer"])

            # Citations
            if show_citations and result["citations"]:
                st.markdown(f"""
                    <hr style="border: none; height: 1px;
                        background: {COLORS['border']}; margin: 12px 0;">
                    <p style="color: {COLORS['accent_secondary']}; font-weight: 600;
                       font-size: 0.85rem; margin-bottom: 8px;">
                       📎 Sources Referenced
                    </p>
                """, unsafe_allow_html=True)

                for i, cite in enumerate(result["citations"], 1):
                    score = cite.get("score", 0)
                    st.markdown(f"""
                        <div class="citation-card">
                            <span class="citation-source">[{i}] {cite['source']}</span>
                            — Page {cite['page']}
                            <span style="float: right; color: {COLORS['text_muted']};">
                                Score: {score:.4f}
                            </span>
                            <div class="citation-preview">
                                {cite.get('chunk_preview', '')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Performance metrics
            st.markdown(f"""
                <div class="perf-bar">
                    ⚡ Retrieval: {result['retrieval_latency_ms']}ms &bull;
                    🕐 Total: {result['total_latency_ms']}ms &bull;
                    📦 Chunks: {result['chunks_retrieved']}
                </div>
            """, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "citations": result["citations"],
        })
