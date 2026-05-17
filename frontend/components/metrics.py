"""
Metrics Display Components
Glassmorphism metric cards for dashboard and page headers.
"""

import streamlit as st


def render_metric_card(icon: str, value, label: str):
    """Render a single glassmorphism metric card."""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def render_metrics_row(metrics: list):
    """Render a row of metric cards.  Each item: (icon, value, label)."""
    cols = st.columns(len(metrics))
    for col, (icon, value, label) in zip(cols, metrics):
        with col:
            render_metric_card(icon, value, label)
