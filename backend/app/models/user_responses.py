from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class UserResponse(Base):
    __tablename__ = "user_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    uid: Mapped[str] = mapped_column(String, ForeignKey("users.uid"), nullable=False, index=True)
    qid: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("quizes.id"), nullable=False, index=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("quiz_sessions.id"), nullable=False, index=True)

    response: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="user_responses")
    question: Mapped["Question"] = relationship("Question", back_populates="user_responses")
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="user_responses")
    quiz_session: Mapped["QuizSession"] = relationship("QuizSession", back_populates="user_responses")
