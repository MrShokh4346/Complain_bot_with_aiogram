import asyncio
from db.base import Base, engine  # assuming you import the correct async engine
from db.models import User 

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    print("Creating database...")
    asyncio.run(init_models())
    print("Done.")
