from fastapi import APIRouter, HTTPException, status

from app.database.session import persist_chat_turn
from app.rag.rag_pipeline import generate_answer
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(payload: ChatRequest) -> dict:
    try:
        result = generate_answer(payload.question)
        persist_chat_turn(
            session_id=payload.session_id,
            question=payload.question,
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
        )
        return result
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat generation failed: {exc}",
        ) from exc