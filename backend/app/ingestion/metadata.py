from __future__ import annotations


def build_metadata(source: str, page: int = 1) -> dict[str, object]:
    return {"source": source, "page": page}
