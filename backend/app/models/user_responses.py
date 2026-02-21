from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class UserResponse(Base):
    __tablename__ = "user_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    participant_id: Mapped[int] = mapped_column(Integer, ForeignKey("participants.id", ondelete="CASCADE"), nullable=False, index=True)

    qid: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False, index=True)

    response: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    participant: Mapped["Participant"] = relationship("Participant", back_populates="user_responses")
    question: Mapped["Question"] = relationship("Question", back_populates="user_responses")
