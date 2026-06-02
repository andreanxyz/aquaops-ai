from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from datetime import datetime
from app.db.database import AsyncSessionLocal
from app.models.pond import Pond, PondStatus
from app.models.worker import Worker, WorkerRole
from app.models.task import Task, TaskType, TaskStatus
from app.models.report import Report
from app.services.whatsapp.client import send_task_to_worker, send_daily_report_to_owner
from app.services.agent.ai_agent import generate_task_instructions, generate_daily_report

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")

async def dispatch_morning_tasks():
    async with AsyncSessionLocal() as db:
        ponds = (await db.execute(select(Pond).where(Pond.status == PondStatus.active))).scalars().all()
        workers = (await db.execute(select(Worker).where(Worker.is_active == True, Worker.role == WorkerRole.worker))).scalars().all()
        if not workers or not ponds:
            return
        for i, pond in enumerate(ponds):
            worker = workers[i % len(workers)]
            task_type = TaskType.feeding
            if pond.last_water_change:
                if (datetime.utcnow() - pond.last_water_change).days >= pond.water_change_days:
                    task_type = TaskType.water_change
            instructions = await generate_task_instructions(task_type.value, pond.name, pond.fish_type.value, pond.fish_count, worker.name)
            task = Task(pond_id=pond.id, worker_id=worker.id, task_type=task_type, status=TaskStatus.sent, description=instructions, scheduled_at=datetime.utcnow())
            db.add(task)
            await send_task_to_worker(worker.phone_number, worker.name, pond.name, instructions)
        await db.commit()
        print(f"Morning tasks dispatched: {len(ponds)} ponds")

async def send_evening_report():
    async with AsyncSessionLocal() as db:
        owner = (await db.execute(select(Worker).where(Worker.role == WorkerRole.owner, Worker.is_active == True))).scalars().first()
        if not owner:
            return
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        tasks_today = (await db.execute(select(Task).where(Task.created_at >= today_start))).scalars().all()
        tasks_done = sum(1 for t in tasks_today if t.status == TaskStatus.done)
        tasks_problem = sum(1 for t in tasks_today if t.status == TaskStatus.problem)
        problems = [t.worker_report for t in tasks_today if t.status == TaskStatus.problem and t.worker_report]
        ponds = (await db.execute(select(Pond).where(Pond.status == PondStatus.active))).scalars().all()
        ponds_summary = [{"name": p.name, "fish_type": p.fish_type.value, "status": p.status.value} for p in ponds]
        report_text = await generate_daily_report(ponds_summary, tasks_done, tasks_problem, problems)
        await send_daily_report_to_owner(owner.phone_number, report_text)
        db.add(Report(date=datetime.utcnow(), summary=report_text, tasks_done=tasks_done, tasks_problem=tasks_problem, sent_to_owner=True))
        await db.commit()
        print("Daily report sent")

def start_scheduler():
    scheduler.add_job(dispatch_morning_tasks, CronTrigger(hour=7, minute=0))
    scheduler.add_job(dispatch_morning_tasks, CronTrigger(hour=16, minute=0))
    scheduler.add_job(send_evening_report, CronTrigger(hour=20, minute=0))
    scheduler.start()
    print("Scheduler started (07:00, 16:00, 20:00 WIB)")
