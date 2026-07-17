from __future__ import annotations

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _coerce_to_document(doc: Document | dict) -> Document:
    if isinstance(doc, Document):
        return doc
    return Document(page_content=doc["page_content"], metadata=doc.get("metadata", {}))


def split_documents(docs: list[Document | dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    coerced_docs = [_coerce_to_document(doc) for doc in docs]
    split_chunks = splitter.split_documents(coerced_docs)

    return [
        {
            "page_content": chunk.page_content,
            "metadata": dict(chunk.metadata),
        }
        for chunk in split_chunks
    ]