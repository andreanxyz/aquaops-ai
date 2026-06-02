from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import webhook, tasks, ponds, workers
from app.db.database import init_db
from app.services.scheduler.task_scheduler import start_scheduler
from app.services.agent.knowledge_base import load_documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    load_documents()
    start_scheduler()
    yield

app = FastAPI(
    title="AquaOps AI",
    description="AI Agent manajemen peternakan ikan via WhatsApp — Garut, Jawa Barat",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(webhook.router, prefix="/webhook", tags=["WhatsApp"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(ponds.router, prefix="/ponds", tags=["Ponds"])
app.include_router(workers.router, prefix="/workers", tags=["Workers"])

@app.get("/")
async def root():
    return {"app": "AquaOps AI", "version": "0.1.0", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
