from langchain_ollama import ChatOllama

from app.core.config import settings

llm = ChatOllama(
    model=settings.llm_model,
    temperature=0.0,
    request_timeout=60,
)