from fastapi import APIRouter, Request, Query, HTTPException
from sqlalchemy import select
from datetime import datetime
from app.db.database import AsyncSessionLocal
from app.models.worker import Worker
from app.models.task import Task, TaskStatus
from app.models.pond import Pond
from app.services.whatsapp.client import parse_incoming_message, send_message
from app.services.agent.ai_agent import handle_worker_message
from app.core.config import settings

router = APIRouter()

@router.get("")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("")
async def receive_message(request: Request):
    payload = await request.json()
    incoming = parse_incoming_message(payload)
    if not incoming or not incoming["text"]:
        return {"status": "ignored"}
    phone = incoming["from"]
    message = incoming["text"]
    async with AsyncSessionLocal() as db:
        worker = await db.execute(
            select(Worker).where(Worker.phone_number == phone, Worker.is_active == True)
        )
        worker = worker.scalars().first()
        if not worker:
            await send_message(phone, "Nomor kamu belum terdaftar. Hubungi supervisor.")
            return {"status": "unregistered"}
        latest_task = await db.execute(
            select(Task).where(
                Task.worker_id == worker.id,
                Task.status.in_([TaskStatus.sent, TaskStatus.in_progress])
            ).order_by(Task.created_at.desc())
        )
        latest_task = latest_task.scalars().first()
        pond_context = ""
        if latest_task:
            pond = await db.get(Pond, latest_task.pond_id)
            if pond:
                pond_context = f"Kolam: {pond.name}, Ikan: {pond.fish_type.value}, Jumlah: {pond.fish_count} ekor"
            lower_msg = message.lower()
            if any(w in lower_msg for w in ["selesai", "done", "beres", "sudah", "ok"]):
                latest_task.status = TaskStatus.done
                latest_task.worker_report = message
                latest_task.completed_at = datetime.utcnow()
            elif any(w in lower_msg for w in ["masalah", "problem", "mati", "sakit", "aneh"]):
                latest_task.status = TaskStatus.problem
                latest_task.worker_report = message
        ai_response = await handle_worker_message(worker.name, message, pond_context)
        if latest_task:
            latest_task.ai_response = ai_response
            await db.commit()
        await send_message(phone, ai_response)
    return {"status": "ok"}
