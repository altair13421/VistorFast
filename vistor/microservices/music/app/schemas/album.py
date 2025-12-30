# app/schemas/album.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AlbumBase(BaseModel):
    title: str = Field(..., example="旅人")
    romaji_title: str | None = Field(None, example="Tabibito")
    release_date: datetime | None = None
    album_art: Optional[str] = None
    artist_id: int


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    romaji_title: Optional[str] = None
    release_date: Optional[datetime] = None
    album_art: Optional[str] = None
    artist_id: Optional[int] = None


# ---------- nested schemas ----------
class SongSummary(BaseModel):
    id: int
    title: str
    romaji_title: Optional[str] = None
    track_number: int | None = None

    class Config:
        orm_mode = True


class ArtistSummary(BaseModel):
    id: int
    name: str
    romaji_name: str

    class Config:
        orm_mode = True


class AlbumRead(AlbumBase):
    id: int
    artist: ArtistSummary
    songs: List[SongSummary] = []

    class Config:
        orm_mode = True
