import asyncio
from app.database import engine, Base
import app.models.mis  # noqa: F401

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables créées avec succès !")
    await engine.dispose()

asyncio.run(main())