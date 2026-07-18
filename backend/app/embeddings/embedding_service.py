from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


class EmbeddingService:
    _instance: HuggingFaceEmbeddings | None = None

    @classmethod
    def get_instance(cls) -> HuggingFaceEmbeddings:
        if cls._instance is None:
            cls._instance = HuggingFaceEmbeddings(
                model_name=settings.embedding_model,
                model_kwargs={"device": "cpu"},
            )
        return cls._instance