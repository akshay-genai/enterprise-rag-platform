from __future__ import annotations

import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.embeddings.embedding_service import embeddings

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    def __init__(self) -> None:
        self.client = None
        self._ready = False
        self._initialize()

    def _initialize(self) -> None:
        try:
            self.client = Chroma(
                collection_name="enterprise_documents",
                embedding_function=embeddings,
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

    def add_documents(self, documents: list[dict]) -> None:
        if not documents or not self._ready:
            return

        coerced_documents = [
            Document(page_content=doc["page_content"], metadata=doc.get("metadata", {}))
            for doc in documents
        ]
        self.client.add_documents(coerced_documents)

    def similarity_search(self, question: str, k: int = 5) -> list:
        if not self._ready:
            return []

        try:
            return self.client.similarity_search(question, k=k)
        except Exception as exc:
            logger.warning("Vectorstore similarity search failed: %s", exc)
            return []

    def get_document_count(self) -> int:
        if not self._ready:
            return 0
        return int(self.client._collection.count())

    def delete_documents(self, ids: list[str] | None = None) -> None:
        if not self._ready:
            return

        if ids is None:
            self.client.delete_collection()
            return
        self.client.delete(ids)


vectorstore = ChromaVectorStore()