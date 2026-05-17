"""
Document Chunking
Splits loaded documents into semantically meaningful chunks with metadata.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.utils.config import CHUNK_SIZE, CHUNK_OVERLAP
from backend.utils.logger import get_logger

logger = get_logger("ingestion.chunker")


def create_chunks(
    documents: List[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Split documents into chunks while preserving and enriching metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = idx
        chunk.metadata["chunk_total"] = len(chunks)

    logger.info(
        f"Created {len(chunks)} chunks from {len(documents)} sections "
        f"(size={chunk_size}, overlap={chunk_overlap})"
    )
    return chunks
