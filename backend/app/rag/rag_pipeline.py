from typing import Any

from app.llm.ollama_client import llm
from app.llm.prompt_templates import build_rag_prompt
from app.retrieval.retriever import retrieve


def generate_answer(question: str) -> dict[str, Any]:
    try:
        docs = retrieve(question, k=8)
    except Exception:
        docs = []

    if not docs:
        return {
            "answer": "I could not find any relevant documents to answer that question.",
            "sources": [],
        }

    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = build_rag_prompt(question=question, context=context)

    try:
        response = llm.invoke(prompt)
        answer = getattr(response, "content", str(response))
    except Exception:
        answer = (
            "I could not reach the Ollama model service, so I am returning a safe fallback response."
        )

    sources = [
        {
            "document": getattr(doc, "metadata", {}).get("source", "unknown"),
            "page": int(getattr(doc, "metadata", {}).get("page", 1)),
        }
        for doc in docs
    ]

    return {
        "answer": answer,
        "sources": sources,
    }