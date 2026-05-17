"""
Document Service
Manages uploaded file metadata and lifecycle.
"""

from typing import List, Dict

from backend.utils.config import UPLOADS_DIR
from backend.utils.logger import get_logger

logger = get_logger("services.document")


class DocumentService:
    """Manages uploaded documents and their metadata."""

    @staticmethod
    def list_uploaded_files() -> List[Dict]:
        """List all files in the uploads directory with metadata."""
        files = []
        if UPLOADS_DIR.exists():
            for f in sorted(UPLOADS_DIR.iterdir()):
                if f.is_file() and not f.name.startswith("."):
                    files.append({
                        "name": f.name,
                        "size_bytes": f.stat().st_size,
                        "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                        "extension": f.suffix.lower(),
                        "path": str(f),
                    })
        return files

    @staticmethod
    def delete_file(filename: str) -> bool:
        """Delete a file from the uploads directory."""
        path = UPLOADS_DIR / filename
        if path.exists():
            path.unlink()
            logger.info(f"Deleted file: {filename}")
            return True
        return False

    @staticmethod
    def get_upload_stats() -> Dict:
        """Aggregate statistics about uploaded files."""
        files = DocumentService.list_uploaded_files()
        total_size = sum(f["size_bytes"] for f in files)
        extensions: Dict[str, int] = {}
        for f in files:
            ext = f["extension"]
            extensions[ext] = extensions.get(ext, 0) + 1

        return {
            "total_files": len(files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_types": extensions,
        }
