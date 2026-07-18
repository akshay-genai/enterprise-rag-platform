from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question to ask the RAG system")
    session_id: str | None = Field(
        default=None,
        description="Optional conversation session identifier for PostgreSQL persistence",
    )
