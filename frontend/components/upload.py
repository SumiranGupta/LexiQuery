"""
Upload Component
Multi-file upload zone with visual feedback.
"""

import streamlit as st
from frontend.components.theme import COLORS


def render_upload_zone():
    """Render the drag-and-drop file upload zone."""
    st.markdown(f"""
        <div style="text-align: center; padding: 8px 0;">
            <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                Drag & drop your documents or click to browse
            </p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.75rem;">
                Supported: PDF, DOCX, PPTX, XLSX, TXT, CSV, Markdown &bull; Max 50 MB per file
            </p>
        </div>
    """, unsafe_allow_html=True)

    return st.file_uploader(
        "Upload Documents",
        type=["pdf", "txt", "csv", "md", "docx", "pptx", "xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )


def render_file_card(file_info: dict):
    """Render a file info card in the document list."""
    ext_icons = {".pdf": "📕", ".txt": "📄", ".csv": "📊", ".md": "📝", ".docx": "📘", ".pptx": "📙", ".xlsx": "📗"}
    icon = ext_icons.get(file_info["extension"], "📄")

    st.markdown(f"""
        <div class="glass-card" style="padding: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div style="flex: 1;">
                    <div style="color: {COLORS['text_primary']}; font-weight: 600;">
                        {file_info['name']}
                    </div>
                    <div style="color: {COLORS['text_muted']}; font-size: 0.8rem;">
                        {file_info['size_mb']} MB &bull; {file_info['extension'].upper()}
                    </div>
                </div>
                <span class="status-badge status-active">Indexed</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
