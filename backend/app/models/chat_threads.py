from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base

class ChatRole(SQLEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatThread(Base):
    __tablename__ = "chat_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    thread_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("quiz_sessions.id"), nullable=False, index=True)
    role: Mapped[ChatRole] = mapped_column(SQLEnum(ChatRole), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    