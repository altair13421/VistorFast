from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.music import Artist
from app.db.engine import AsyncSessionLocal, SessionLocal
from faster.services.music.app.db.base import SessionLocal


