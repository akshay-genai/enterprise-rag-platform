from __future__ import annotations

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.embeddings.embedding_service import embeddings


class ChromaVectorStore:
    def __init__(self) -> None:
        self.client = Chroma(
            collection_name="enterprise_documents",
            embedding_function=embeddings,
            persist_directory=str(settings.db_dir),
        )

    def add_documents(self, documents: list[dict]) -> None:
        if not documents:
            return

        coerced_documents = [
            Document(page_content=doc["page_content"], metadata=doc.get("metadata", {}))
            for doc in documents
        ]
        self.client.add_documents(coerced_documents)

    def similarity_search(self, question: str, k: int = 5) -> list:
        try:
            return self.client.similarity_search(question, k=k)
        except Exception:
            return []

    def get_document_count(self) -> int:
        return int(self.client._collection.count())

    def delete_documents(self, ids: list[str] | None = None) -> None:
        if ids is None:
            self.client.delete_collection()
            return
        self.client.delete(ids)


vectorstore = ChromaVectorStore()