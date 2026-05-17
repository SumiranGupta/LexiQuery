"""
LexiQuery — FastAPI Backend API
RESTful API wrapping all backend services for the React frontend.
"""

import shutil
import platform
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.vectorstores.faiss_store import FAISSStore
from backend.rag.retriever import Retriever
from backend.rag.chain import RAGChain
from backend.ingestion.pipeline import IngestionPipeline
from backend.services.analytics_service import AnalyticsService
from backend.services.document_service import DocumentService
from backend.services.query_service import QueryService
from backend.utils.config import (
    EMBEDDING_MODEL, LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP,
    TOP_K_RESULTS, GROQ_API_KEY, UPLOADS_DIR, VECTORSTORE_DIR,
    SUPPORTED_EXTENSIONS,
)
from backend.utils.logger import get_logger

logger = get_logger("api")

# ── Initialize services ────────────────────────────────────────────
analytics = AnalyticsService()
vector_store = FAISSStore()
retriever = Retriever(vector_store)
rag_chain = RAGChain(retriever)
ingestion = IngestionPipeline(vector_store, analytics)
query_svc = QueryService(rag_chain, analytics)
doc_svc = DocumentService()

# ── FastAPI app ─────────────────────────────────────────────────────
app = FastAPI(title="LexiQuery API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic models ────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str
    top_k: int = 5


# ── Stats & Analytics ──────────────────────────────────────────────

@app.get("/api/stats")
def get_stats():
    """Aggregate analytics stats."""
    return analytics.get_stats()


@app.get("/api/upload-stats")
def get_upload_stats():
    """File system upload stats."""
    return doc_svc.get_upload_stats()


@app.get("/api/top-sources")
def get_top_sources(limit: int = Query(5)):
    """Top documents by chunk count."""
    return analytics.get_top_sources(limit)


# ── Documents ──────────────────────────────────────────────────────

@app.get("/api/documents")
def list_documents():
    """List all documents from analytics DB."""
    return analytics.get_documents()


@app.get("/api/files")
def list_files():
    """List uploaded files from filesystem."""
    return doc_svc.list_uploaded_files()


@app.post("/api/upload")
def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process multiple documents. Sync so it runs in threadpool and won't block event loop."""
    results = []
    for uploaded in files:
        ext = Path(uploaded.filename).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            results.append({
                "filename": uploaded.filename,
                "status": "error",
                "error": f"Unsupported file type: {ext}",
            })
            continue

        # Save to temp then use ingestion pipeline
        dest = UPLOADS_DIR / uploaded.filename
        try:
            content = uploaded.file.read()
            with open(dest, "wb") as f:
                f.write(content)

            # Create a simple wrapper mimicking Streamlit's UploadedFile
            class _FakeUpload:
                def __init__(self, name, size, path):
                    self.name = name
                    self.size = size
                    self._path = path

                def getbuffer(self):
                    return open(self._path, "rb").read()

            fake = _FakeUpload(uploaded.filename, len(content), str(dest))
            # Directly load, chunk, embed, index
            from backend.ingestion.loaders import load_document
            from backend.ingestion.chunker import create_chunks
            import time

            start = time.time()
            documents = load_document(dest)
            chunks = create_chunks(documents)
            vector_store.add_documents(chunks)
            elapsed = time.time() - start

            record = {
                "filename": uploaded.filename,
                "file_size": len(content),
                "page_count": len(documents),
                "chunk_count": len(chunks),
                "processing_time_s": round(elapsed, 2),
            }
            analytics.record_document(record)
            record["status"] = "success"
            results.append(record)

        except Exception as e:
            results.append({
                "filename": uploaded.filename,
                "status": "error",
                "error": str(e),
            })

    return {"results": results}


@app.delete("/api/files/{filename}")
def delete_file(filename: str):
    """Delete a file, remove from analytics, and rebuild FAISS index from remaining files."""
    try:
        if not doc_svc.delete_file(filename):
            raise HTTPException(status_code=404, detail="File not found")

        # Remove from analytics DB
        analytics.delete_document(filename)

        # Rebuild FAISS from all remaining files so deleted content is gone
        from backend.ingestion.loaders import load_document
        from backend.ingestion.chunker import create_chunks

        remaining = doc_svc.list_uploaded_files()
        vector_store.reset()

        for file_info in remaining:
            try:
                docs = load_document(file_info["path"])
                chunks = create_chunks(docs)
                vector_store.add_documents(chunks)
            except Exception as e:
                logger.warning(f"Skipped {file_info.get('name')} during rebuild: {e}")

        return {
            "status": "deleted",
            "filename": filename,
            "remaining_files": len(remaining),
            "vectors_rebuilt": vector_store.total_vectors,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete failed for {filename!r}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ── Queries ────────────────────────────────────────────────────────

@app.post("/api/ask")
def ask_question(req: AskRequest):
    """Process a RAG query."""
    if not vector_store.is_initialized:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed. Upload documents first.",
        )
    try:
        return query_svc.ask(req.question, top_k=req.top_k)
    except Exception as e:
        msg = str(e)
        if "rate_limit_exceeded" in msg or "429" in msg or "RateLimit" in type(e).__name__:
            # Extract wait time if present
            import re
            wait = re.search(r"try again in ([\d]+m[\d.]+s)", msg)
            detail = "Groq API daily token limit reached."
            if wait:
                detail += f" Please try again in {wait.group(1)}."
            raise HTTPException(status_code=429, detail=detail)
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=msg)


@app.get("/api/queries")
def get_queries(limit: int = Query(50)):
    """Get recent query history."""
    return analytics.get_recent_queries(limit)


# ── System ─────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """System health information."""
    return {
        "checks": [
            {
                "name": "FAISS Vector Store",
                "healthy": vector_store.is_initialized,
                "detail": f"{vector_store.total_vectors} vectors",
            },
            {
                "name": "Groq API Key",
                "healthy": bool(GROQ_API_KEY),
                "detail": "Configured" if GROQ_API_KEY else "Missing",
            },
            {
                "name": "Uploads Directory",
                "healthy": UPLOADS_DIR.exists(),
                "detail": str(UPLOADS_DIR),
            },
            {
                "name": "Vector Store Directory",
                "healthy": VECTORSTORE_DIR.exists(),
                "detail": str(VECTORSTORE_DIR),
            },
        ],
        "config": {
            "llm_model": LLM_MODEL,
            "embedding_model": EMBEDDING_MODEL,
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
            "top_k": TOP_K_RESULTS,
        },
        "system": {
            "python": platform.python_version(),
            "os": f"{platform.system()} {platform.release()}",
            "arch": platform.machine(),
            "vector_db": "FAISS",
            "llm_provider": "Groq",
        },
        "vectors": vector_store.total_vectors,
    }


@app.post("/api/reset")
def reset_system():
    """Reset vector store and analytics."""
    vector_store.reset()
    analytics.clear_all()
    return {"status": "reset"}


@app.post("/api/reset-queries")
def reset_queries():
    """Clear query history."""
    analytics.clear_queries()
    return {"status": "queries_cleared"}


# ── Serve React build (production) ─────────────────────────────────
react_build = Path(__file__).parent / "react-frontend" / "dist"
if react_build.exists():
    app.mount("/assets", StaticFiles(directory=str(react_build / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        """Serve React SPA for all non-API routes."""
        file_path = react_build / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(react_build / "index.html"))
