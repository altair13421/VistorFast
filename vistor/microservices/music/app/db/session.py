# app/db/session.py
from contextlib import asynccontextmanager
from app.db.engine import AsyncSessionLocal


@asynccontextmanager
async def get_async_session():
    """
    FastAPI dependency that yields an AsyncSession and guarantees a clean close.
    Usage:

        @router.get(...)
        async def endpoint(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
