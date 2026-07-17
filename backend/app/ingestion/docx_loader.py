from pathlib import Path

from docx import Document


def load_docx(path: str) -> list[dict]:
    document = Document(path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    text = "\n".join(paragraphs)

    return [
        {
            "page_content": text,
            "metadata": {"source": Path(path).name, "page": 1},
        }
    ]
