from sqlalchemy import Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.database import Base

class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    summary: Mapped[str] = mapped_column(Text)
    tasks_done: Mapped[int] = mapped_column(Integer, default=0)
    tasks_problem: Mapped[int] = mapped_column(Integer, default=0)
    ai_analysis: Mapped[str] = mapped_column(Text, nullable=True)
    sent_to_owner: Mapped[bool] = mapped_column(Integer, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
