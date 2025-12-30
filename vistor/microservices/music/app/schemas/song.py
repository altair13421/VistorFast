# app/schemas/song.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SongBase(BaseModel):
    title: str = Field(..., example="旅人")
    romaji_title: str | None = None
    file_location: str | None = None  # path or URL
    duration: int | None = None        # seconds
    track_number: int | None = None
    times_played: int | None = None
    created_at: datetime | None = None
    album_id: Optional[int] = None


class SongCreate(SongBase):
    pass


class SongUpdate(BaseModel):
    title: Optional[str] = None
    romaji_title: Optional[str] = None
    file_location: Optional[str] = None
    duration: Optional[int] = None
    track_number: Optional[int] = None
    times_played: Optional[int] = None
    album_id: Optional[int] = None


# ---------- nested schemas ----------
class GenreSummary(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ArtistSummary(BaseModel):
    id: int
    name: str
    romaji_name: str

    class Config:
        orm_mode = True


class AlbumSummary(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class SongsDisplayable(SongBase):
    id: int
    album: Optional[AlbumSummary] = []
    genres: List[GenreSummary] = []
    artists: List[ArtistSummary] = []

    class Config:
        orm_mode = True
