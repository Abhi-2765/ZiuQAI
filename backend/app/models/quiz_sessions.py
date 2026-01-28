from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("quizes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False, index=True)

    quiz_start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    quiz_duration: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="quiz_sessions")
    user: Mapped["User"] = relationship("User", back_populates="quiz_sessions")
    user_responses: Mapped[List["UserResponse"]] = relationship("UserResponse", back_populates="quiz_session")
