"""
Analytics Chart Components
Plotly-based charts — theme-aware for dark & light modes.
"""

import streamlit as st
import plotly.graph_objects as go
from frontend.components.theme import COLORS


def _layout():
    """Return Plotly layout dict with current theme colors."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=COLORS["chart_text"]),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
    )


def render_query_timeline(queries: list):
    """Bar chart showing query volume per day."""
    if not queries:
        st.info("No query data yet — start asking questions!")
        return

    dates = [q.get("created_at", "")[:10] for q in queries]
    counts: dict = {}
    for d in dates:
        counts[d] = counts.get(d, 0) + 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(counts.keys()),
        y=list(counts.values()),
        mode="lines+markers",
        line=dict(color=COLORS["chart_line"], width=2),
        marker=dict(size=8, color=COLORS["accent_secondary"]),
        fill="tozeroy",
        fillcolor=COLORS["chart_fill"],
    ))
    fig.update_layout(**_layout(), title="Query Activity")
    fig.update_xaxes(gridcolor=COLORS["chart_grid"])
    fig.update_yaxes(gridcolor=COLORS["chart_grid"])
    st.plotly_chart(fig, use_container_width=True)


def render_latency_chart(queries: list):
    """Bar chart showing retrieval latency of recent queries."""
    if not queries:
        st.info("No latency data yet.")
        return

    latencies = [q.get("retrieval_latency_ms", 0) for q in queries[-20:]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(1, len(latencies) + 1)),
        y=latencies,
        marker=dict(
            color=latencies,
            colorscale=[[0, COLORS["accent_primary"]], [1, COLORS["accent_secondary"]]],
        ),
    ))
    fig.update_layout(**_layout(), title="Retrieval Latency (ms)")
    fig.update_xaxes(title_text="Query #", gridcolor=COLORS["chart_grid"])
    fig.update_yaxes(gridcolor=COLORS["chart_grid"])
    st.plotly_chart(fig, use_container_width=True)


def render_document_distribution(documents: list):
    """Donut chart of document types in the knowledge base."""
    if not documents:
        st.info("No documents uploaded yet.")
        return

    ext_counts: dict = {}
    for doc in documents:
        name = doc.get("filename", "")
        ext = name.rsplit(".", 1)[-1].upper() if "." in name else "OTHER"
        ext_counts[ext] = ext_counts.get(ext, 0) + 1

    fig = go.Figure(data=[go.Pie(
        labels=list(ext_counts.keys()),
        values=list(ext_counts.values()),
        hole=0.5,
        marker=dict(colors=COLORS["chart_pie"]),
        textinfo="label+percent",
        textfont=dict(color=COLORS["chart_pie_text"]),
    )])
    fig.update_layout(**_layout(), title="Document Types", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
