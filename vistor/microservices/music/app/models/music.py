from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base

class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    romaji_name = Column(String, index=True)
    created_at = Column(DateTime, index=True)

    @property
    def full_name(self) -> str:
        return f"{self.name} ({self.romaji_name})"


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(ForeignKey("artists.id"))

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column()
    
