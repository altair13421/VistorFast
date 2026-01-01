from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.models.music import Artist
from app.db.engine import AsyncSessionLocal
from app.db.base import SessionLocal

from typing import Dict, Any, List

router = APIRouter()

@router.get("/artists")
def all_artists(db: Depends(SessionLocal)) -> List:
    return JSONResponse([{
        "status": "ok"
    }])

