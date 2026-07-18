from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConversationRecord:
    id: int | None = None
    session_id: str | None = None
    created_at: datetime | None = None


@dataclass
class MessageRecord:
    id: int | None = None
    conversation_id: int | None = None
    role: str | None = None
    content: str | None = None
    created_at: datetime | None = None
