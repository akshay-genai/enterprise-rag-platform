from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Original user query")
    response: str = Field(..., min_length=1, description="Assistant response")
    rating: int = Field(..., ge=1, le=5, description="Feedback score from 1 to 5")
    comments: str | None = Field(default=None, description="Optional feedback comments")
