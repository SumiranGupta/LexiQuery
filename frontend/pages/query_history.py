"""
Query History Page
Browse and review past queries and AI responses.
"""

import streamlit as st
from frontend.components.theme import COLORS


def render(analytics_service):
    """Render the query history page."""
    st.markdown('<div class="page-header">📋 Query History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Browse your past queries and AI responses</div>',
        unsafe_allow_html=True,
    )

    queries = analytics_service.get_recent_queries(50)

    if not queries:
        st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 60px;">
                <span style="font-size: 2.5rem;">🔍</span>
                <p style="color: {COLORS['text_secondary']}; margin-top: 12px; font-size: 1.1rem;">
                    No queries yet
                </p>
                <p style="color: {COLORS['text_muted']}; font-size: 0.85rem;">
                    Head to the AI Assistant to start asking questions
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    # ── Summary ─────────────────────────────────────────────────────
    total = len(queries)
    avg_latency = sum(q.get("total_latency_ms", 0) for q in queries) / max(total, 1)
    avg_chunks = sum(q.get("chunks_retrieved", 0) for q in queries) / max(total, 1)

    cols = st.columns(3)
    with cols[0]:
        st.metric("Total Queries", total)
    with cols[1]:
        st.metric("Avg Latency", f"{avg_latency:.0f}ms")
    with cols[2]:
        st.metric("Avg Chunks Retrieved", f"{avg_chunks:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Query List ──────────────────────────────────────────────────
    for q in queries:
        label = q["query_text"][:100]
        if len(q["query_text"]) > 100:
            label += "..."

        with st.expander(f"🔹 {label}", expanded=False):
            st.markdown(f"""
                <div style="color: {COLORS['text_muted']}; font-size: 0.8rem; margin-bottom: 8px;">
                    📅 {q.get('created_at', 'N/A')} &bull;
                    ⚡ {q.get('total_latency_ms', 0):.0f}ms &bull;
                    📦 {q.get('chunks_retrieved', 0)} chunks
                </div>
            """, unsafe_allow_html=True)

            st.markdown("**Question:**")
            st.markdown(q["query_text"])

            if q.get("response_preview"):
                st.markdown("**Response:**")
                st.markdown(q["response_preview"])
