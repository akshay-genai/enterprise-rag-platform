from __future__ import annotations

import sqlite3

import psycopg

from app.core.config import settings


class PostgresRepository:
    """Small repository wrapper for the PostgreSQL-backed chat tables.

    When PostgreSQL is unavailable during local/test execution, the repository
    automatically falls back to a local SQLite database so the app remains
    importable and the API can still respond to smoke tests.
    """

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

    _sqlite_schema_sql = """
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        rating INTEGER NOT NULL,
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
        self._sqlite_path = settings.db_dir / "enterprise_rag.sqlite3"
        self._use_sqlite = False
        self.init_schema()

    def _connect(self):
        if self._use_sqlite:
            self._sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            return sqlite3.connect(self._sqlite_path)

        try:
            if settings.postgres_dsn:
                return psycopg.connect(settings.postgres_dsn)
            return psycopg.connect(**self._connection_kwargs)
        except psycopg.OperationalError:
            self._use_sqlite = True
            self._sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            return sqlite3.connect(self._sqlite_path)

    def init_schema(self) -> None:
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    if self._use_sqlite:
                        conn.executescript(self._sqlite_schema_sql)
                    else:
                        cursor.execute(self._schema_sql)
        except Exception:
            self._use_sqlite = True
            self._sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self._sqlite_path) as conn:
                conn.executescript(self._sqlite_schema_sql)

    def create_or_get_conversation(self, session_id: str | None) -> int:
        if not session_id:
            session_id = "default-session"

        with self._connect() as conn:
            with conn.cursor() as cursor:
                if self._use_sqlite:
                    cursor.execute(
                        "INSERT OR IGNORE INTO conversations (session_id) VALUES (?)",
                        (session_id,),
                    )
                    cursor.execute(
                        "SELECT id FROM conversations WHERE session_id = ?",
                        (session_id,),
                    )
                else:
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
        with self._connect() as conn:
            with conn.cursor() as cursor:
                if self._use_sqlite:
                    cursor.execute(
                        "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                        (conversation_id, role, content),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO messages (conversation_id, role, content)
                        VALUES (%s, %s, %s)
                        """,
                        (conversation_id, role, content),
                    )

    def save_feedback(self, query: str, response: str, rating: int, comments: str | None) -> dict[str, str | int]:
        with self._connect() as conn:
            with conn.cursor() as cursor:
                if self._use_sqlite:
                    cursor.execute(
                        "INSERT INTO feedback (query, response, rating, comments) VALUES (?, ?, ?, ?)",
                        (query, response, rating, comments),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO feedback (query, response, rating, comments)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (query, response, rating, comments),
                    )

        return {"status": "saved", "rating": rating}


repository = PostgresRepository()
