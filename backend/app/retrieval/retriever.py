from app.vectorstore.chroma_store import vectorstore


def retrieve(question: str, k: int = 5):
    try:
        return vectorstore.similarity_search(question, k=k)
    except Exception:
        return []