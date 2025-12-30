from sqlalchemy.orm import Session
from app.models.music import Song
from app.schemas.song import SongsDisplayable

def get_track_info(db: Session, song_id: int) -> SongsDisplayable:
    return db.query(Song).filter(Song.id == song_id).first()
