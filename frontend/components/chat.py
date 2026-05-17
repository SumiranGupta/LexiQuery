"""
Chat Interface Component
Renders chat messages with optional citation cards.
"""

import streamlit as st
from frontend.components.theme import COLORS


def render_chat_message(role: str, content: str, citations=None):
    """Render a single chat message with optional citations."""
    with st.chat_message(role):
        st.markdown(content)

        if citations:
            st.markdown(f"""
                <hr style="border: none; height: 1px;
                    background: {COLORS['border']}; margin: 12px 0;">
                <p style="color: {COLORS['accent_secondary']}; font-weight: 600;
                   font-size: 0.85rem; margin-bottom: 8px;">
                   📎 Sources Referenced
                </p>
            """, unsafe_allow_html=True)

            for i, cite in enumerate(citations, 1):
                score = cite.get("score", 0)
                st.markdown(f"""
                    <div class="citation-card">
                        <span class="citation-source">[{i}] {cite['source']}</span>
                        — Page {cite['page']}
                        <span style="float: right; color: {COLORS['text_muted']};">
                            Score: {score:.4f}
                        </span>
                        <div class="citation-preview">{cite.get('chunk_preview', '')}</div>
                    </div>
                """, unsafe_allow_html=True)


def render_chat_input():
    """Render the chat input box and return user text."""
    return st.chat_input("Ask anything about your documents...")
