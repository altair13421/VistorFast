from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.music import Song, Artist, Album, Genre
from app.db.session import get_db

router = APIRouter()

@router.get("/songs/{song_id}")
def read_song(song_id: int, db: Session = Depends(get_db)):
    # Placeholder implementation
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song
