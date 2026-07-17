from fastapi import APIRouter, HTTPException, status

from app.rag.rag_pipeline import generate_answer
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(payload: ChatRequest) -> dict:
    try:
        return generate_answer(payload.question)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat generation failed: {exc}",
        ) from exc