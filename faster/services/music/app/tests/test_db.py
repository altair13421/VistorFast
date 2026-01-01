from app.db.engine import init_db
import asyncio

async def test_db():
    await init_db()
    print("DB initialized!")
