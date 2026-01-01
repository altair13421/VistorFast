from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from app.db.engine import init_db, engine


origins = [
    "http://localhost",
    "http://localhost:3000",
]
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code that runs *before* the first request (startup)
    await init_db()          # ← your DB‑initialisation helper
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")
