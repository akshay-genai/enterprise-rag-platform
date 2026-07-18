import logging

from app.vectorstore.chroma_store import vectorstore

logger = logging.getLogger(__name__)


def retrieve(question: str, k: int = 5):
    try:
        return vectorstore.similarity_search(question, k=k)
    except Exception as exc:
        logger.warning("Retrieval failed safely and returned no results: %s", exc)
        return []