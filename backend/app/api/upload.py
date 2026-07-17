from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.ingestion.chunking import split_documents
from app.ingestion.docx_loader import load_docx
from app.ingestion.metadata import build_metadata
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.txt_loader import load_txt
from app.vectorstore.chroma_store import vectorstore

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
async def upload_document(file: UploadFile = File(...)) -> dict[str, str]:
    allowed_suffixes = {".pdf", ".docx", ".txt"}
    file_suffix = Path(file.filename or "").suffix.lower()

    if file_suffix not in allowed_suffixes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOCX, and TXT files are supported.",
        )

    storage_dir = settings.upload_dir
    storage_dir.mkdir(parents=True, exist_ok=True)

    destination = storage_dir / file.filename
    content = await file.read()
    destination.write_bytes(content)

    try:
        if file_suffix == ".pdf":
            documents = load_pdf(str(destination))
        elif file_suffix == ".docx":
            documents = load_docx(str(destination))
        else:
            documents = load_txt(str(destination))

        chunks = split_documents(documents)
        vectorstore.add_documents(chunks)

        return {
            "message": "Document uploaded and indexed successfully.",
            "filename": file.filename,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document ingestion failed: {exc}",
        ) from exc