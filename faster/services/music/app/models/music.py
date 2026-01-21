from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

song_artists = Table(
    "song_artists",
    Base.metadata,
    Column("artist_id", ForeignKey("artists.id"), primary_key=True),
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
)

song_genres = Table(
    "song_genres",
    Base.metadata,
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
)

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    romaji_name = Column(String, index=True)
    created_at = Column(DateTime, index=True, default=datetime.datetime.now(datetime.timezone.utc))
    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", secondary="song_artists", back_populates="artists")


    @property
    def full_name(self) -> str:
        return f"{self.name} ({self.romaji_name})"

    @property
    def stats(self):
        return {
            "total_albums": len(self.albums),
            "total_songs": sum(len(album.songs) for album in self.albums),
            "times_played": sum(song.times_played for song in self.songs),
        }


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    songs = relationship("Song", secondary="song_genres", back_populates="genre")
    created_at = Column(DateTime, index=True, default=datetime.datetime.now(datetime.timezone.utc))

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    romaji_title = Column(String, index=True)
    release_date = Column(DateTime, index=True)
    created_at = Column(DateTime, index=True, default=datetime.datetime.now(datetime.timezone.utc))
    artist_id = Column(ForeignKey("artists.id"))
    album_art = Column(String)
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    romaji_title = Column(String, index=True)

    # Metadata
    file_path = Column(String, index=True)
    duration = Column(Integer, index=True)  # duration in seconds
    track_number = Column(Integer, index=True)
    times_played = Column(Integer, index=True, default=0)
    created_at = Column(DateTime, index=True, default=datetime.datetime.now(datetime.timezone.utc))

    # Relations
    genres = relationship(Genre, secondary="song_genre_association", back_populates="songs")
    artists = relationship("Artist", secondary="song_artists", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    album_id = Column(ForeignKey("albums.id"))


    
    # adding a New Comment