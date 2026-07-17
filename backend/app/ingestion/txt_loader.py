from pathlib import Path


def load_txt(path: str) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    return [
        {
            "page_content": text,
            "metadata": {"source": Path(path).name, "page": 1},
        }
    ]
