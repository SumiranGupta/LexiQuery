"""
Sidebar Navigation Component
Enterprise-style navigation with branding, quick info, and theme toggle.
"""

import streamlit as st
from frontend.components.theme import COLORS

PAGES = {
    "Dashboard": "📊",
    "Upload Center": "📁",
    "AI Assistant": "🤖",
    "Query History": "📋",
    "System Status": "⚙️",
}


def render_sidebar() -> str:
    """Render the sidebar and return the selected page name."""
    with st.sidebar:
        # ── Brand ───────────────────────────────────────────────────
        st.markdown("""
            <div style="text-align: center; padding: 16px 0 8px 0;">
                <div class="brand-title">⚡ LexiQuery</div>
                <div class="brand-subtitle">AI Knowledge Platform</div>
            </div>
            <hr class="styled-divider">
        """, unsafe_allow_html=True)

        # ── Navigation ──────────────────────────────────────────────
        st.markdown(f"""
            <p style="color: {COLORS['text_muted']}; font-size: 0.7rem;
               text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
               Navigation
            </p>
        """, unsafe_allow_html=True)

        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"

        for page_name, icon in PAGES.items():
            if st.button(
                f"{icon}  {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
            ):
                st.session_state.current_page = page_name
                st.rerun()

        st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

        # ── Quick Info ──────────────────────────────────────────────
        st.markdown(f"""
            <p style="color: {COLORS['text_muted']}; font-size: 0.7rem;
               text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
               Tech Stack
            </p>
            <div style="font-size: 0.8rem; color: {COLORS['text_secondary']}; line-height: 1.8;">
                🧠 Model: <strong style="color: {COLORS['text_primary']}">Llama 3.3 70B</strong><br>
                🔗 Embeddings: <strong style="color: {COLORS['text_primary']}">MiniLM-L6</strong><br>
                💾 Vector DB: <strong style="color: {COLORS['text_primary']}">FAISS</strong><br>
                ⚡ Inference: <strong style="color: {COLORS['text_primary']}">Groq</strong>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)

        # ── Theme Toggle ────────────────────────────────────────────
        if "theme_mode" not in st.session_state:
            st.session_state.theme_mode = "dark"

        current = st.session_state.theme_mode
        is_dark = current == "dark"

        st.markdown(f"""
            <p style="color: {COLORS['text_muted']}; font-size: 0.7rem;
               text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
               Appearance
            </p>
        """, unsafe_allow_html=True)

        toggle_label = "🌙 Dark Mode" if is_dark else "☀️ Light Mode"
        switch_label = "Switch to Light" if is_dark else "Switch to Dark"

        if st.button(f"{switch_label}", key="theme_toggle", use_container_width=True):
            st.session_state.theme_mode = "light" if is_dark else "dark"
            st.rerun()

        st.markdown(f"""
            <div style="text-align: center; margin-top: 4px; font-size: 0.75rem;
                        color: {COLORS['text_muted']};">
                Currently: {toggle_label}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='styled-divider'>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="text-align: center; font-size: 0.7rem; color: {COLORS['text_muted']};">
                LexiQuery v2.0 • Enterprise Edition
            </div>
        """, unsafe_allow_html=True)

    return st.session_state.current_page
