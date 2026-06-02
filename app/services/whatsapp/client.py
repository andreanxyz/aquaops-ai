import httpx
from app.core.config import settings

WHATSAPP_API_URL = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_ID}/messages"

async def send_message(to: str, message: str) -> dict:
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(WHATSAPP_API_URL, json=payload, headers=headers)
        return response.json()

async def send_task_to_worker(worker_phone: str, worker_name: str, pond_name: str, task_description: str) -> dict:
    message = (
        f"🐟 *AquaOps AI - Tugas Hari Ini*\n\n"
        f"Halo {worker_name}!\n\n"
        f"📋 *Kolam:* {pond_name}\n"
        f"📝 *Tugas:* {task_description}\n\n"
        f"Setelah selesai, balas pesan ini dengan laporan singkat.\n"
        f"Jika ada masalah, langsung ceritakan!"
    )
    return await send_message(worker_phone, message)

async def send_daily_report_to_owner(owner_phone: str, report_text: str) -> dict:
    message = f"📊 *Laporan Harian AquaOps*\n\n{report_text}"
    return await send_message(owner_phone, message)

def parse_incoming_message(payload: dict) -> dict | None:
    try:
        entry = payload["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        if "messages" not in value:
            return None
        msg = value["messages"][0]
        contact = value["contacts"][0]
        return {
            "from": msg["from"],
            "name": contact["profile"]["name"],
            "message_id": msg["id"],
            "type": msg["type"],
            "text": msg.get("text", {}).get("body", "") if msg["type"] == "text" else "",
            "timestamp": msg["timestamp"],
        }
    except (KeyError, IndexError):
        return None
