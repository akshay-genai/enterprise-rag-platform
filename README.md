# Enterprise RAG Platform

Enterprise-grade Retrieval-Augmented Generation (RAG) system for intelligent document search, semantic retrieval, citation-based answer generation, and admin-style document workflows using open-source LLMs and modern Python + React tooling.

## Overview

This repository contains a full-stack enterprise RAG application with:

- FastAPI backend for ingestion, retrieval, chat orchestration, and dashboard APIs
- React + Vite frontend for chat, upload, and admin experiences
- Chroma-based vector storage for semantic retrieval
- Ollama-backed LLM integration for local inference
- Python document loaders and chunking pipeline for ingestion

## Tech Stack

- Backend: Python, FastAPI, Pydantic, LangChain, Chroma, sentence-transformers
- Frontend: React, Vite, Material UI, Axios
- LLM runtime: Ollama
- Storage: local file system + Chroma vector database

## Repository Structure

- `backend/` — FastAPI app, agents, ingestion, retrieval, and vectorstore code
- `frontend/` — React app source and build config
- `data/` — sample and uploaded document assets
- `db/` — local vector database files and persisted state
- `tests/` — backend test suite

## Local Setup

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

### 3. Environment Configuration

Copy the sample environment file and customize it for your local machine:

```bash
copy .env.example .env
```

## Environment Variables

The repository uses a simple `.env.example` template for local configuration. Keep secrets and machine-specific values in your local `.env` file only.

Recommended values to define locally:

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `EMBEDDING_MODEL`
- `COLLECTION_NAME`
- `UPLOAD_DIR`
- `VECTOR_DB_PATH`

## Suggested Git Workflow

Use a clean branching model so the project remains easy to evolve:

- `main` — production-stable code
- `develop` — integration branch for the next release
- `feature/*` — new functionality and enhancements
- `bugfix/*` — non-breaking defect fixes
- `hotfix/*` — urgent fixes for `main`
- `release/*` — final stabilization before release

### Recommended PR flow

1. Create a feature branch from `develop`
2. Commit small, reviewable changes
3. Open a PR into `develop`
4. Merge to `develop` after code review
5. Merge `develop` into `main` for a production release

## Future Enhancement Plan

Ideal next enhancement areas for this app:

- Add authentication and role-based admin access
- Add background ingestion jobs and async document processing
- Improve retrieval quality with hybrid re-ranking and metadata filters
- Add observability, logs, and request tracing
- Containerize with Docker and Docker Compose
- Add CI/CD linting and test automation

## Notes for Public Repository Push

Before pushing:

- Keep local secrets out of git
- Never commit the real `.env` file
- Avoid committing generated Chroma or runtime database state
- Prefer versioning only source code, config templates, and sample assets

## License

This project is intended for internal/demo use unless a separate license is added later.
