from sqlalchemy import String, Float, Integer, Enum, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.database import Base
import enum

class FishType(str, enum.Enum):
    nila = "nila"
    gurame = "gurame"
    lele = "lele"
    mas = "mas"

class PondStatus(str, enum.Enum):
    active = "active"
    maintenance = "maintenance"
    empty = "empty"

class Pond(Base):
    __tablename__ = "ponds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    fish_type: Mapped[FishType] = mapped_column(Enum(FishType), default=FishType.nila)
    fish_count: Mapped[int] = mapped_column(Integer, default=0)
    size_m2: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[PondStatus] = mapped_column(Enum(PondStatus), default=PondStatus.active)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    feeding_schedule: Mapped[str] = mapped_column(String(50), default="07:00,16:00")
    water_change_days: Mapped[int] = mapped_column(Integer, default=7)
    sorting_interval_days: Mapped[int] = mapped_column(Integer, default=30)
    last_water_change: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_sorting: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
