from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session, joinedload, subqueryload
from app.models.music import Song
from app.schemas.song import SongsDisplayable
from app.db.session import get_db
from app.core.song_handler import scan_directory

router = APIRouter()

@router.post("/songs/scan/")
def scan_directory_for_songs(directory_path: str, db: Session = Depends(get_db)):
    # Logic to scan the directory and add songs to the database
    # This is a placeholder implementation
    # In a real implementation, you would walk the directory,
    # read song files, extract metadata, and store them in the DB.
    return {"message": f"Scanned directory: {directory_path}"}


@router.get("/songs/{song_id}/info/", response_model=SongsDisplayable)
def read_song(song_id: int, db: Session = Depends(get_db)):
    # Fetch the song with its related data using relationships
    song_query = db.query(Song).filter(Song.id == song_id)

    # Use `.options()` to load related objects eagerly (avoid N+1 query problem)
    song = song_query.options(
        joinedload(Song.album),  # 1:1 Album if linked directly
        subqueryload(Song.artists),  # Many-to-many Artist relationship
        subqueryload(
            Song.genres
        ),  # Many-to-many Genre relation (if using a secondary table)
    ).first()

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {
        "name": song.name,
        "romaji_name": song.romaji_name,
        "duration": song.duration,
        "artist": [
            {"id": artist.id, "name": artist.name} for artist in song.artists
        ],  # Access artist via the relationship
        "album": song.album.title if song.album else None,
        "genres": [
            genre.name for genre in song.genres
        ],  # Example of accessing many-to-many
    }


@router.get("/songs/{song_id}/stream/")
def stream_song(song_id: int, db: Session = Depends(get_db)):
    song: Song | None = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    file_path = song.file_path  # Assuming `file_path` is a field in the Song model
    try:
        return FileResponse(path=file_path, media_type="audio/mpeg", filename=song.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming song: {str(e)}")
