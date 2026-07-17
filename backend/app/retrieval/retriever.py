from app.vectorstore.chroma_store import vectorstore


def retrieve(question: str, k: int = 5):
    return vectorstore.similarity_search(question, k=k)