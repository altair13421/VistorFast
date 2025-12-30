from sqlalchemy.orm import Session
from app.models.music import Song
from app.schemas.song import SongCreate, SongUpdate

def get_song(db: Session, song_id: int):
    return db.query(Song).filter(Song.id == song_id).first()

def create_song(db: Session, song: SongCreate):
    db_song = Song(
        title=song.title,
        duration=song.duration,
        album_id=song.album_id,
        times_played=song.times_played
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def update_song(db: Session, db_song: Song, song_update: SongUpdate):
    if song_update.title is not None:
        db_song.title = song_update.title
    if song_update.duration is not None:
        db_song.duration = song_update.duration
    if song_update.album_id is not None:
        db_song.album_id = song_update.album_id
    if song_update.times_played is not None:
        db_song.times_played = song_update.times_played
    db.commit()
    db.refresh(db_song)
    return db_song

def delete_song(db: Session, song_id: int):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    db.delete(db_song)
    db.commit()
    return db_song
