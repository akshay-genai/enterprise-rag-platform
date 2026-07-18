from fastapi import APIRouter, HTTPException, status

from app.database.repository import repository
from app.schemas.feedback import FeedbackRequest

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/")
async def submit_feedback(payload: FeedbackRequest) -> dict[str, str | int]:
    try:
        return repository.save_feedback(
            query=payload.query,
            response=payload.response,
            rating=payload.rating,
            comments=payload.comments,
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Feedback persistence failed: {exc}",
        ) from exc
