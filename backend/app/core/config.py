from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


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

    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db = os.getenv("POSTGRES_DB", "postgres")
    postgres_user = os.getenv("POSTGRES_USER", "postgres")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_dsn = os.getenv("POSTGRES_DSN") or os.getenv("DATABASE_URL")


settings = Settings()
