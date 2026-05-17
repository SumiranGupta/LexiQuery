"""
Dashboard Page
Platform overview with key metrics and analytics visualizations.
"""

import streamlit as st

from frontend.components.metrics import render_metrics_row
from frontend.components.analytics import (
    render_query_timeline,
    render_latency_chart,
    render_document_distribution,
)
from frontend.components.theme import COLORS


def render(analytics_service):
    """Render the dashboard page."""
    st.markdown('<div class="page-header">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Platform overview and real-time analytics</div>',
        unsafe_allow_html=True,
    )

    # ── Key Metrics ─────────────────────────────────────────────────
    stats = analytics_service.get_stats()

    render_metrics_row([
        ("📄", stats["total_documents"], "Documents"),
        ("🧩", stats["total_chunks"], "Chunks"),
        ("💬", stats["total_queries"], "Queries"),
        ("⚡", f'{stats["avg_retrieval_latency_ms"]}ms', "Avg Latency"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──────────────────────────────────────────────────────
    queries = analytics_service.get_recent_queries(50)
    documents = analytics_service.get_documents()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_query_timeline(queries)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_latency_chart(queries)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_document_distribution(documents)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
            <p style="color: {COLORS['text_primary']}; font-weight: 600; margin-bottom: 12px;">
                🏆 Top Documents
            </p>
        """, unsafe_allow_html=True)

        top_sources = analytics_service.get_top_sources()
        if top_sources:
            for doc in top_sources:
                st.markdown(f"""
                    <div style="padding: 8px 0; border-bottom: 1px solid {COLORS['border']};">
                        <div style="color: {COLORS['text_primary']}; font-size: 0.85rem;">
                            📕 {doc['filename']}
                        </div>
                        <div style="color: {COLORS['text_muted']}; font-size: 0.75rem;">
                            {doc['page_count']} pages &bull; {doc['chunk_count']} chunks
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <p style="color: {COLORS['text_muted']}; font-size: 0.85rem;">
                    No documents indexed yet. Head to Upload Center to get started.
                </p>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
