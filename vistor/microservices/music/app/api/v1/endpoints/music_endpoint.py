from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, subqueryload
from app.models.music import Song, Artist, Album, Genre
from app.db.session import get_db

router = APIRouter()
@router.get("/songs/{song_id}")
def read_song(song_id: int, db: Session = Depends(get_db)):
    # Fetch the song with its related data using relationships
    song_query = db.query(Song).filter(Song.id == song_id)
    
    # Use `.options()` to load related objects eagerly (avoid N+1 query problem)
    song = song_query.options(
        joinedload(Song.artists),         # 1:1 Artist relationship
        joinedload(Song.album),          # 1:1 Album if linked directly
        subqueryload(Song.genres)         # Many-to-many Genre relation (if using a secondary table)
    ).first()

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {
        "song": song,
        "artist": song.artist.name,  # Access artist via the relationship
        "album": song.album.title if song.album else None,
        "genres": [genre.name for genre in song.genres]  # Example of accessing many-to-many
    }
