# app/schemas/artist.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ArtistBase(BaseModel):
    name: str = Field(..., example="坂本龍一")
    romaji_name: str = Field(..., example="Ryuichi Sakamoto")
    created_at: datetime | None = None  # will be set by DB if omitted


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    romaji_name: Optional[str] = None
    created_at: Optional[datetime] = None


# ---------- nested schemas for relations ----------
class AlbumSummary(BaseModel):
    id: int
    title: str
    romaji_title: str | None = None
    release_date: datetime | None = None

    class Config:
        orm_mode = True


class SongSummary(BaseModel):
    id: int
    title: str
    romaji_title: Optional[str] = None
    track_number: int | None = None

    class Config:
        orm_mode = True


class ArtistRead(ArtistBase):
    id: int
    albums: List[AlbumSummary] = []
    songs: List[SongSummary] = []

    # computed properties from the model
    full_name: str
    stats: dict[str, int]

    class Config:
        orm_mode = True
