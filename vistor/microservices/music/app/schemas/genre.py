# app/schemas/genre.py
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class GenreBase(BaseModel):
    name: str = Field(..., example="Jazz")


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Optional[str] = None


# ---------- nested schemas ----------
class SongSummary(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class GenreRead(GenreBase):
    id: int
    songs: List[SongSummary] = []

    class Config:
        orm_mode = True
