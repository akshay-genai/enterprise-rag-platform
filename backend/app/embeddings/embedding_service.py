from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    _instance: HuggingFaceEmbeddings | None = None

    @classmethod
    def get_instance(cls) -> HuggingFaceEmbeddings:
        if cls._instance is None:
            cls._instance = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-en-v1.5",
                model_kwargs={"device": "cpu"},
            )
        return cls._instance


embeddings = EmbeddingService.get_instance()