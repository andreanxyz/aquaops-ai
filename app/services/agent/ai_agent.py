import anthropic
from app.core.config import settings
from app.services.agent.knowledge_base import query_knowledge

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Kamu adalah AquaOps AI, asisten cerdas untuk manajemen peternakan ikan di Garut, Jawa Barat.
Tugasmu membantu pekerja tambak dengan panduan praktis berdasarkan SOP budidaya.
Gunakan Bahasa Indonesia sederhana, jawaban singkat dan langsung bisa dilakukan.
Gunakan emoji secukupnya. Jika darurat, tulis DARURAT di awal pesan."""

async def handle_worker_message(worker_name: str, message: str, pond_context: str = "") -> str:
    kb_context = query_knowledge(message)
    user_content = f"""Pesan dari pekerja {worker_name}: "{message}"
{f"Konteks kolam: {pond_context}" if pond_context else ""}
{f"Referensi SOP:\n{kb_context}" if kb_context else ""}
Berikan respons yang tepat dan praktis."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text

async def generate_task_instructions(task_type: str, pond_name: str, fish_type: str, fish_count: int, worker_name: str) -> str:
    task_map = {
        "feeding": f"pemberian pakan ikan {fish_type}",
        "water_change": f"penggantian air kolam {fish_type}",
        "sorting": f"pemilahan ikan {fish_type}",
        "health_check": f"pengecekan kesehatan ikan {fish_type}",
    }
    kb_context = query_knowledge(f"cara {task_map.get(task_type, task_type)}")
    prompt = f"""Buatkan instruksi singkat untuk pekerja {worker_name}:
- Tugas: {task_map.get(task_type, task_type)}
- Kolam: {pond_name}, Ikan: {fish_type}, Jumlah: {fish_count} ekor
Referensi SOP: {kb_context}
Format: max 5 langkah, emoji, bahasa mudah dipahami."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

async def generate_daily_report(ponds_summary: list, tasks_done: int, tasks_problem: int, problems_detail: list) -> str:
    pond_info = "\n".join([f"- {p['name']} ({p['fish_type']}): {p['status']}" for p in ponds_summary])
    problems_info = "\n".join(problems_detail) if problems_detail else "Tidak ada masalah"
    prompt = f"""Buat laporan harian singkat untuk pemilik tambak:
Kondisi kolam:\n{pond_info}
Statistik: selesai={tasks_done}, masalah={tasks_problem}
Detail masalah: {problems_info}
Format: ringkas, max 200 kata, sertakan rekomendasi jika ada masalah."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
