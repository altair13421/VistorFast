from sqlalchemy.orm import Session
from app.models.music import Artist
from app.schemas.artist import ArtistCreate, ArtistUpdate

def get_artist(db: Session, artist_id: int):
    return db.query(Artist).filter(Artist.id == artist_id).first()

def create_artist(db: Session, artist: ArtistCreate):
    db_artist = Artist(
        name=artist.name,
        romaji_name=artist.romaji_name,
        created_at=artist.created_at
    )
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def update_artist(db: Session, db_artist: Artist, artist_update: ArtistUpdate):
    if artist_update.name is not None:
        db_artist.name = artist_update.name
    if artist_update.romaji_name is not None:
        db_artist.romaji_name = artist_update.romaji_name
    if artist_update.created_at is not None:
        db_artist.created_at = artist_update.created_at
    db.commit()
    db.refresh(db_artist)
    return db_artist

def delete_artist(db: Session, artist_id: int):
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    db.delete(db_artist)
    db.commit()
    return db_artist


