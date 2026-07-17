from __future__ import annotations

from pathlib import Path


class Settings:
    """Application configuration values used across the backend."""

    backend_root = Path(__file__).resolve().parents[2]
    project_root = backend_root.parent
    data_dir = project_root / "data"
    upload_dir = data_dir / "documents"
    db_dir = project_root / "db"
    collection_name = "enterprise_documents"
    model_name = "BAAI/bge-small-en-v1.5"
    llm_model = "llama3.2:1b"


settings = Settings()
