"""
Upload Center Page
Document upload, processing pipeline, and file management.
"""

import streamlit as st

from frontend.components.upload import render_upload_zone, render_file_card
from frontend.components.metrics import render_metrics_row
from frontend.components.theme import COLORS


def render(ingestion_pipeline, document_service, analytics_service):
    """Render the upload center page."""
    st.markdown('<div class="page-header">📁 Upload Center</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Upload and manage your knowledge base documents</div>',
        unsafe_allow_html=True,
    )

    # ── Stats ───────────────────────────────────────────────────────
    upload_stats = document_service.get_upload_stats()
    db_stats = analytics_service.get_stats()

    render_metrics_row([
        ("📄", upload_stats["total_files"], "Files Uploaded"),
        ("💾", f'{upload_stats["total_size_mb"]} MB', "Total Size"),
        ("🧩", db_stats["total_chunks"], "Total Chunks"),
        ("📊", db_stats["total_pages"], "Total Pages"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Upload + Info ───────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
            <p style="color: {COLORS['text_primary']}; font-weight: 600;
               font-size: 1.1rem; margin-bottom: 8px;">
                📤 Upload Documents
            </p>
        """, unsafe_allow_html=True)

        uploaded_files = render_upload_zone()

        if uploaded_files:
            if st.button("🚀 Process & Index Documents", use_container_width=True):
                with st.spinner("Processing documents..."):
                    progress = st.progress(0)
                    results = []

                    for i, file in enumerate(uploaded_files):
                        progress.progress(
                            (i + 1) / len(uploaded_files),
                            text=f"Processing {file.name}...",
                        )
                        try:
                            result = ingestion_pipeline.ingest_file(file)
                            result["status"] = "success"
                        except Exception as e:
                            result = {
                                "filename": file.name,
                                "status": "error",
                                "error": str(e),
                            }
                        results.append(result)

                    progress.empty()

                    success = [r for r in results if r["status"] == "success"]
                    errors = [r for r in results if r["status"] == "error"]

                    if success:
                        total_chunks = sum(r.get("chunk_count", 0) for r in success)
                        st.success(
                            f"✅ Processed {len(success)} file(s) — "
                            f"{total_chunks} chunks indexed"
                        )
                    if errors:
                        for err in errors:
                            st.error(f"❌ {err['filename']}: {err['error']}")

                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: {COLORS['text_primary']}; font-weight: 600; margin-bottom: 12px;">
                    ℹ️ Supported Formats
                </p>
                <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem; line-height: 2;">
                    📕 PDF Documents<br>
                    📘 Word Documents (.docx)<br>
                    📙 PowerPoint (.pptx)<br>
                    📗 Excel (.xlsx)<br>
                    📄 Plain Text (.txt)<br>
                    📊 CSV Spreadsheets<br>
                    📝 Markdown (.md)
                </div>
                <hr class="styled-divider">
                <p style="color: {COLORS['text_primary']}; font-weight: 600; margin-bottom: 8px;">
                    🔧 Processing Pipeline
                </p>
                <div style="color: {COLORS['text_muted']}; font-size: 0.8rem; line-height: 1.8;">
                    1. Document Loading<br>
                    2. Text Extraction<br>
                    3. Smart Chunking<br>
                    4. Embedding Generation<br>
                    5. Vector Indexing
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ── Indexed Documents ───────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
        <p style="color: {COLORS['text_primary']}; font-weight: 600; font-size: 1.1rem;">
            📚 Indexed Documents
        </p>
    """, unsafe_allow_html=True)

    files = document_service.list_uploaded_files()
    if files:
        for file_info in files:
            render_file_card(file_info)
    else:
        st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 40px;">
                <span style="font-size: 2rem;">📭</span>
                <p style="color: {COLORS['text_secondary']}; margin-top: 8px;">
                    No documents uploaded yet. Upload your first document above.
                </p>
            </div>
        """, unsafe_allow_html=True)
