from sqlalchemy.orm import Session
from app.models.music import Genre
from app.schemas.genre import GenreCreate, GenreUpdate

def get_genre(db: Session, genre_id: int):
    return db.query(Genre).filter(Genre.id == genre_id).first()

def create_genre(db: Session, genre: GenreCreate):
    db_genre = Genre(
        name=genre.name
    )
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def update_genre(db: Session, db_genre: Genre, genre_update: GenreUpdate):
    if genre_update.name is not None:
        db_genre.name = genre_update.name
    db.commit()
    db.refresh(db_genre)
    return db_genre

def delete_genre(db: Session, genre_id: int):
    db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
    db.delete(db_genre)
    db.commit()
    return db_genre


