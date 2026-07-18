from __future__ import annotations

import logging

import psycopg

from app.core.config import settings

logger = logging.getLogger(__name__)


class PostgresRepository:
    """Small repository wrapper for the new PostgreSQL-backed chat tables."""

    _schema_sql = """
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(255) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        conversation_id INT NOT NULL,
        role VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_messages_conversation
            FOREIGN KEY (conversation_id)
            REFERENCES conversations(id)
            ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        rating INT NOT NULL,
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    def __init__(self) -> None:
        self._connection_kwargs = {
            "host": settings.postgres_host,
            "port": settings.postgres_port,
            "dbname": settings.postgres_db,
            "user": settings.postgres_user,
            "password": settings.postgres_password,
        }
        self._enabled = True
        self._disabled_reason: str | None = None
        self.init_schema()

    def _connect(self):
        if not self._enabled:
            raise RuntimeError(self._disabled_reason or "Postgres repository is unavailable")

        if settings.postgres_dsn:
            return psycopg.connect(settings.postgres_dsn)
        return psycopg.connect(**self._connection_kwargs)

    def init_schema(self) -> None:
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(self._schema_sql)
        except Exception as exc:
            self._enabled = False
            self._disabled_reason = f"Postgres unavailable: {exc}"
            logger.warning(
                "Postgres repository disabled during startup; chat persistence will be skipped. Reason: %s",
                exc,
            )

    def create_or_get_conversation(self, session_id: str | None) -> int:
        if not self._enabled:
            return 0

        if not session_id:
            session_id = "default-session"

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO conversations (session_id)
                    VALUES (%s)
                    ON CONFLICT (session_id) DO NOTHING
                    """,
                    (session_id,),
                )
                cursor.execute(
                    "SELECT id FROM conversations WHERE session_id = %s",
                    (session_id,),
                )
                result = cursor.fetchone()
                return int(result[0])

    def add_message(self, conversation_id: int, role: str, content: str) -> None:
        if not self._enabled:
            return

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO messages (conversation_id, role, content)
                    VALUES (%s, %s, %s)
                    """,
                    (conversation_id, role, content),
                )

    def save_feedback(self, query: str, response: str, rating: int, comments: str | None) -> dict[str, str | int]:
        if not self._enabled:
            logger.warning("Feedback persistence skipped because Postgres repository is unavailable.")
            return {"status": "saved", "rating": rating}

        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO feedback (query, response, rating, comments)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (query, response, rating, comments),
                )

        return {"status": "saved", "rating": rating}


repository = PostgresRepository()
