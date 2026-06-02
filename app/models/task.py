from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.database import Base
import enum

class TaskType(str, enum.Enum):
    feeding = "feeding"
    water_change = "water_change"
    sorting = "sorting"
    health_check = "health_check"
    treatment = "treatment"

class TaskStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    in_progress = "in_progress"
    done = "done"
    problem = "problem"

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pond_id: Mapped[int] = mapped_column(Integer, ForeignKey("ponds.id"))
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey("workers.id"))
    task_type: Mapped[TaskType] = mapped_column(Enum(TaskType))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.pending)
    description: Mapped[str] = mapped_column(Text)
    worker_report: Mapped[str] = mapped_column(Text, nullable=True)
    ai_response: Mapped[str] = mapped_column(Text, nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
