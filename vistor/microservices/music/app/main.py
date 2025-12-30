from fastapi import FastAPI
from app.api.v1.endpoints.music_endpoint import router as music_router
from app.api.v1.endpoints.meta_endpoints import router as meta_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(music_router, prefix="/music", tags=["music"])
app.include_router(meta_router, prefix="/meta", tags=["meta"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
