from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime
from app.db.database import get_db
from app.models.task import Task, TaskStatus

router = APIRouter()

class TaskResponse(BaseModel):
    id: int
    pond_id: int
    worker_id: int
    task_type: str
    status: str
    description: str
    worker_report: str = None
    ai_response: str = None
    scheduled_at: datetime
    class Config:
        from_attributes = True

@router.get("", response_model=list[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    return result.scalars().all()

@router.get("/today", response_model=list[TaskResponse])
async def today_tasks(db: AsyncSession = Depends(get_db)):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    result = await db.execute(select(Task).where(Task.created_at >= today))
    return result.scalars().all()
