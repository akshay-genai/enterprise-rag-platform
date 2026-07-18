from langchain_ollama import ChatOllama

from app.core.config import settings

llm = ChatOllama(
    model=settings.llm_model,
    base_url=settings.ollama_base_url,
    temperature=0.0,
    request_timeout=60,
)