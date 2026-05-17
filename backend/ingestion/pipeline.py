"""
Ingestion Pipeline
Orchestrates the full document ingestion workflow:
    file save → load → chunk → embed → index → record analytics
"""

import time
from pathlib import Path
from typing import Dict, Any, List

from backend.utils.config import UPLOADS_DIR
from backend.utils.logger import get_logger
from backend.ingestion.loaders import load_document
from backend.ingestion.chunker import create_chunks

logger = get_logger("ingestion.pipeline")


class IngestionPipeline:
    """End-to-end document ingestion — from raw upload to indexed vectors."""

    def __init__(self, vector_store, analytics_service):
        self.vector_store = vector_store
        self.analytics = analytics_service

    def save_uploaded_file(self, uploaded_file) -> Path:
        """Persist a Streamlit UploadedFile to the uploads directory."""
        dest = UPLOADS_DIR / uploaded_file.name
        with open(dest, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logger.info(f"Saved uploaded file: {dest.name}")
        return dest

    def ingest_file(self, uploaded_file) -> Dict[str, Any]:
        """Run the full ingestion pipeline for a single file."""
        start = time.time()

        file_path = self.save_uploaded_file(uploaded_file)
        documents = load_document(file_path)
        chunks = create_chunks(documents)
        self.vector_store.add_documents(chunks)

        elapsed = time.time() - start

        record = {
            "filename": uploaded_file.name,
            "file_size": uploaded_file.size,
            "page_count": len(documents),
            "chunk_count": len(chunks),
            "processing_time_s": round(elapsed, 2),
        }
        self.analytics.record_document(record)

        logger.info(
            f"Ingested {uploaded_file.name}: {len(documents)} pages, "
            f"{len(chunks)} chunks in {elapsed:.1f}s"
        )
        return record

    def ingest_multiple(self, uploaded_files) -> List[Dict[str, Any]]:
        """Ingest a batch of uploaded files."""
        results = []
        for f in uploaded_files:
            try:
                result = self.ingest_file(f)
                result["status"] = "success"
            except Exception as e:
                logger.error(f"Failed to ingest {f.name}: {e}")
                result = {"filename": f.name, "status": "error", "error": str(e)}
            results.append(result)
        return results
