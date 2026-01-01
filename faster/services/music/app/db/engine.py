
import sqlalchemy.ext.asyncio as async_sqlalchemy
from app.core.config import settings
# ------------------------------------------------------------------
DATABASE_URL = (
    settings.database_url  # e.g., "postgresql+asyncpg://user:password@localhost/dbname"
)

engine = async_sqlalchemy.create_async_engine(
    DATABASE_URL,
    echo=True,          # Log SQL statements – handy during dev
    future=True,
)

# Create a session factory that returns an AsyncSession
AsyncSessionLocal = async_sqlalchemy.async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    from models.music import metadata
    """Create tables on first run. In production you’d use Alembic."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
