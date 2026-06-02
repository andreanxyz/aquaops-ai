from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.db.database import get_db
from app.models.pond import Pond, FishType, PondStatus

router = APIRouter()

class PondCreate(BaseModel):
    name: str
    fish_type: FishType = FishType.nila
    fish_count: int = 0
    size_m2: float = 0.0
    feeding_schedule: str = "07:00,16:00"
    water_change_days: int = 7
    sorting_interval_days: int = 30
    notes: str = None

class PondResponse(BaseModel):
    id: int
    name: str
    fish_type: str
    fish_count: int
    size_m2: float
    status: str
    feeding_schedule: str
    water_change_days: int
    notes: str = None
    class Config:
        from_attributes = True

@router.get("", response_model=list[PondResponse])
async def list_ponds(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pond))
    return result.scalars().all()

@router.post("", response_model=PondResponse)
async def create_pond(data: PondCreate, db: AsyncSession = Depends(get_db)):
    pond = Pond(**data.model_dump())
    db.add(pond)
    await db.commit()
    await db.refresh(pond)
    return pond

@router.get("/{pond_id}", response_model=PondResponse)
async def get_pond(pond_id: int, db: AsyncSession = Depends(get_db)):
    pond = await db.get(Pond, pond_id)
    if not pond:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")
    return pond
