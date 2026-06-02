from sqlalchemy import String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.database import Base
import enum

class WorkerRole(str, enum.Enum):
    owner = "owner"
    supervisor = "supervisor"
    worker = "worker"

class Worker(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    role: Mapped[WorkerRole] = mapped_column(Enum(WorkerRole), default=WorkerRole.worker)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
