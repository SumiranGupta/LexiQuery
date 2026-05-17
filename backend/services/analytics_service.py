"""
Analytics Service
Tracks documents, queries, and system metrics using SQLite.
Lightweight — zero external dependencies beyond Python stdlib.
"""

import sqlite3
import json
import uuid
from typing import Dict, Any, List

from backend.utils.config import ANALYTICS_DB_PATH
from backend.utils.logger import get_logger

logger = get_logger("services.analytics")


class AnalyticsService:
    """Lightweight analytics powered by SQLite."""

    def __init__(self, db_path=ANALYTICS_DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Create tables if they don't exist."""
        conn = self._conn()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    file_size INTEGER DEFAULT 0,
                    page_count INTEGER DEFAULT 0,
                    chunk_count INTEGER DEFAULT 0,
                    processing_time_s REAL DEFAULT 0,
                    uploaded_at TEXT DEFAULT (datetime('now')),
                    status TEXT DEFAULT 'active'
                );

                CREATE TABLE IF NOT EXISTS queries (
                    id TEXT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    response_preview TEXT,
                    chunks_retrieved INTEGER DEFAULT 0,
                    retrieval_latency_ms REAL DEFAULT 0,
                    total_latency_ms REAL DEFAULT 0,
                    sources_referenced TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                );
            """)
            conn.commit()
            logger.info("Analytics database initialized")
        finally:
            conn.close()

    # ── Write Operations ────────────────────────────────────────────

    def record_document(self, doc: Dict[str, Any]):
        """Record a document ingestion event (upsert — replaces previous entry for same filename)."""
        conn = self._conn()
        try:
            # Remove previous record for the same filename to prevent duplicates
            conn.execute("DELETE FROM documents WHERE filename = ?", (doc["filename"],))
            conn.execute(
                "INSERT INTO documents "
                "(id, filename, file_size, page_count, chunk_count, processing_time_s) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    str(uuid.uuid4()),
                    doc["filename"],
                    doc.get("file_size", 0),
                    doc.get("page_count", 0),
                    doc.get("chunk_count", 0),
                    doc.get("processing_time_s", 0),
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def record_query(self, query_data: Dict[str, Any]):
        """Record a query event."""
        conn = self._conn()
        try:
            sources = json.dumps(query_data.get("citations", []))
            conn.execute(
                "INSERT INTO queries "
                "(id, query_text, response_preview, chunks_retrieved, "
                "retrieval_latency_ms, total_latency_ms, sources_referenced) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    str(uuid.uuid4()),
                    query_data["query"],
                    query_data.get("answer", "")[:500],
                    query_data.get("chunks_retrieved", 0),
                    query_data.get("retrieval_latency_ms", 0),
                    query_data.get("total_latency_ms", 0),
                    sources,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    # ── Read Operations ─────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Aggregate analytics statistics."""
        conn = self._conn()
        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT COUNT(DISTINCT filename), COALESCE(SUM(page_count), 0), "
                "COALESCE(SUM(chunk_count), 0) FROM documents"
            )
            doc_count, total_pages, total_chunks = cur.fetchone()

            cur.execute(
                "SELECT COUNT(*), COALESCE(AVG(retrieval_latency_ms), 0), "
                "COALESCE(AVG(total_latency_ms), 0) FROM queries"
            )
            query_count, avg_retrieval_ms, avg_total_ms = cur.fetchone()

            return {
                "total_documents": doc_count,
                "total_pages": total_pages,
                "total_chunks": total_chunks,
                "total_queries": query_count,
                "avg_retrieval_latency_ms": round(avg_retrieval_ms, 1),
                "avg_total_latency_ms": round(avg_total_ms, 1),
            }
        finally:
            conn.close()

    def get_recent_queries(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return the most recent queries."""
        conn = self._conn()
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM queries ORDER BY created_at DESC LIMIT ?", (limit,)
            )
            return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def get_documents(self) -> List[Dict[str, Any]]:
        """Return all indexed documents."""
        conn = self._conn()
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
            return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def get_top_sources(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Return the most-chunked documents (deduplicated by filename)."""
        conn = self._conn()
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT filename, "
                "SUM(page_count) as page_count, "
                "SUM(chunk_count) as chunk_count, "
                "MAX(uploaded_at) as uploaded_at "
                "FROM documents GROUP BY filename "
                "ORDER BY chunk_count DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def get_unique_document_count(self) -> int:
        """Return count of unique document filenames."""
        conn = self._conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(DISTINCT filename) FROM documents")
            return cur.fetchone()[0]
        finally:
            conn.close()

    # ── Delete Operations ───────────────────────────────────────────

    def delete_document(self, filename: str):
        """Remove analytics records for a specific file by filename."""
        conn = self._conn()
        try:
            conn.execute("DELETE FROM documents WHERE filename = ?", (filename,))
            conn.commit()
            logger.info(f"Deleted analytics record for: {filename}")
        finally:
            conn.close()

    def clear_documents(self):
        """Remove all document records from analytics."""
        conn = self._conn()
        try:
            conn.execute("DELETE FROM documents")
            conn.commit()
            logger.info("Cleared all document records from analytics")
        finally:
            conn.close()

    def clear_queries(self):
        """Remove all query records from analytics."""
        conn = self._conn()
        try:
            conn.execute("DELETE FROM queries")
            conn.commit()
            logger.info("Cleared all query records from analytics")
        finally:
            conn.close()

    def clear_all(self):
        """Remove all analytics data."""
        self.clear_documents()
        self.clear_queries()
