from __future__ import annotations

from app.database.repository import repository


def persist_chat_turn(session_id: str | None, question: str, answer: str, sources: list[dict[str, object]]) -> None:
    conversation_id = repository.create_or_get_conversation(session_id)
    repository.add_message(conversation_id, "user", question)
    repository.add_message(conversation_id, "assistant", answer)
