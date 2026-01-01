from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from app.db.engine import init_db, engine

from app.api.v1.endpoints.meta import router as meta_router
from app.models.music import Base
from sqlalchemy import text

origins = [
    "http://localhost",
    "http://localhost:3000",
]
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Optional: Check if database is initialized
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        await conn.commit()
    yield                   # ← this is where the app starts handling requests
    # Code that runs *after* the last request (shutdown)
    await engine.dispose()  # close the connection pool

app = FastAPI(lifespan=lifespan, title="Async PostgreSQL Music Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meta_router, prefix="/meta", tags=["Meta"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")
