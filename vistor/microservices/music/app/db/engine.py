# app/db/engine.py
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from app.core.config import settings


# -----------------------
# 1. Sync engine (kept for legacy code/tests)
# -----------------------
SYNC_ENGINE: Engine = create_engine(settings.database_url, echo=False, future=True)

# -----------------------
# 2. Async engine
# -----------------------
ASYNC_ENGINE: AsyncEngine = create_async_engine(
    settings.database_url,
    # Recommended pool size options for Postgres:
    pool_size=20,
    max_overflow=0,
    # If you need a different echo level per environment:
    echo=settings.log_level == "debug",
)

# -----------------------
# 3. Async session factory
# -----------------------
AsyncSessionLocal = async_sessionmaker(
    bind=ASYNC_ENGINE, expire_on_commit=False, class_=AsyncSession  # <- see note below
)
