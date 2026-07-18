from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.dashboard import router as dashboard_router
from app.api.feedback import router as feedback_router
from app.api.upload import router as upload_router

app = FastAPI(title="Enterprise RAG Platform", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def health_check() -> dict[str, str]:
    return {"status": "healthy"}


def root_health() -> dict[str, str]:
    return {"status": "running"}


app.add_api_route("/health", health_check, methods=["GET"])
app.add_api_route("/", root_health, methods=["GET"])
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(dashboard_router)
app.include_router(feedback_router)
