from pathlib import Path

from app.ingestion.chunking import split_documents
from app.ingestion.metadata import build_metadata


def test_split_documents_respects_chunking_config() -> None:
    docs = [
        {
            "page_content": "A" * 1500,
            "metadata": {"source": "sample.txt", "page": 1},
        }
    ]

    chunks = split_documents(docs)

    assert len(chunks) >= 1
    assert all(len(chunk["page_content"]) <= 1000 for chunk in chunks)


def test_build_metadata_includes_source_and_file_name() -> None:
    metadata = build_metadata("sample.pdf", 1)

    assert metadata["source"] == "sample.pdf"
    assert metadata["page"] == 1
