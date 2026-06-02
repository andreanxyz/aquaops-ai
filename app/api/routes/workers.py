from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.db.database import get_db
from app.models.worker import Worker, WorkerRole

router = APIRouter()

class WorkerCreate(BaseModel):
    name: str
    phone_number: str
    role: WorkerRole = WorkerRole.worker

class WorkerResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    role: str
    is_active: bool
    class Config:
        from_attributes = True

@router.get("", response_model=list[WorkerResponse])
async def list_workers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Worker).where(Worker.is_active == True))
    return result.scalars().all()

@router.post("", response_model=WorkerResponse)
async def create_worker(data: WorkerCreate, db: AsyncSession = Depends(get_db)):
    worker = Worker(**data.model_dump())
    db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker

@router.delete("/{worker_id}")
async def deactivate_worker(worker_id: int, db: AsyncSession = Depends(get_db)):
    worker = await db.get(Worker, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Pekerja tidak ditemukan")
    worker.is_active = False
    await db.commit()
    return {"message": f"Pekerja {worker.name} dinonaktifkan"}
