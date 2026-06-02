import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.database import AsyncSessionLocal, init_db
from app.models.pond import Pond, FishType
from app.models.worker import Worker, WorkerRole

async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        db.add(Worker(name="Pak Hendra", phone_number="6281234567890", role=WorkerRole.owner))
        for name, phone in [("Asep","6281234567891"),("Budi","6281234567892"),("Cecep","6281234567893")]:
            db.add(Worker(name=name, phone_number=phone, role=WorkerRole.worker))
        for name, fish, count, size in [
            ("Kolam A", FishType.nila, 500, 50.0),
            ("Kolam B", FishType.nila, 400, 40.0),
            ("Kolam C", FishType.gurame, 200, 30.0),
            ("Kolam D", FishType.gurame, 150, 25.0),
        ]:
            db.add(Pond(name=name, fish_type=fish, fish_count=count, size_m2=size))
        await db.commit()
        print("Seed data berhasil! 1 owner, 3 pekerja, 4 kolam")
        print("Ganti nomor WhatsApp di file ini sebelum production!")

asyncio.run(seed())
