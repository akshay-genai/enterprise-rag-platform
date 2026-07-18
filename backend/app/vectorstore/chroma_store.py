from __future__ import annotations

import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    def __init__(self) -> None:
        self.client = None
        self._ready = False
        self._initializing = False

    def _ensure_ready(self) -> None:
        if self._ready or self._initializing:
            return

        self._initializing = True
        try:
            from app.embeddings.embedding_service import EmbeddingService

            self.client = Chroma(
                collection_name=settings.collection_name,
                embedding_function=EmbeddingService.get_instance(),
                persist_directory=str(settings.db_dir),
            )
            self._ready = True
        except Exception as exc:
            logger.warning(
                "Vectorstore initialization failed; retrieval will be treated as empty. Reason: %s",
                exc,
            )
            self.client = None
            self._ready = False
        finally:
            self._initializing = False

    def add_documents(self, documents: list[dict]) -> None:
        if not documents:
            return

        self._ensure_ready()
        if not self._ready:
            return

        coerced_documents = [
            Document(page_content=doc["page_content"], metadata=doc.get("metadata", {}))
            for doc in documents
        ]
        self.client.add_documents(coerced_documents)

    def similarity_search(self, question: str, k: int = 5) -> list:
        self._ensure_ready()
        if not self._ready:
            return []

        try:
            return self.client.similarity_search(question, k=k)
        except Exception as exc:
            logger.warning("Vectorstore similarity search failed: %s", exc)
            return []

    def get_document_count(self) -> int:
        self._ensure_ready()
        if not self._ready:
            return 0
        return int(self.client._collection.count())

    def delete_documents(self, ids: list[str] | None = None) -> None:
        self._ensure_ready()
        if not self._ready:
            return

        if ids is None:
            self.client.delete_collection()
            return
        self.client.delete(ids)


vectorstore = ChromaVectorStore()