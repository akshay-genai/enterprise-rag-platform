from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    message: str
    filename: str = Field(..., description="Uploaded document filename")
