from sqlalchemy.orm import Session
from app.models.music import Album
from app.schemas.album import AlbumCreate, AlbumUpdate

def get_album(db: Session, album_id: int):
    return db.query(Album).filter(Album.id == album_id).first()

def create_album(db: Session, album: AlbumCreate):
    db_album = Album(
        title=album.title,
        artist_id=album.artist_id,
        album_art=album.album_art
    )
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def update_album(db: Session, db_album: Album, album_update: AlbumUpdate):
    if album_update.title is not None:
        db_album.title = album_update.title
    if album_update.artist_id is not None:
        db_album.artist_id = album_update.artist_id
    if album_update.album_art is not None:
        db_album.album_art = album_update.album_art
    db.commit()
    db.refresh(db_album)
    return db_album

def delete_album(db: Session, album_id: int):
    db_album = db.query(Album).filter(Album.id == album_id).first()
    db.delete(db_album)
    db.commit()
    return db_album
