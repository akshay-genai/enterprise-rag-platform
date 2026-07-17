from fastapi import APIRouter

from app.core.config import settings
from app.vectorstore.chroma_store import vectorstore

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
def get_dashboard_stats() -> dict[str, int | str]:
    return {
        "documents_indexed": vectorstore.get_document_count(),
        "active_sessions": 1,
        "llm_model": settings.llm_model,
    }
