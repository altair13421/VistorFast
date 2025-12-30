from sqlalchemy.orm import Session
from app.models.music import Genre

def get_genre(db: Session, genre_id: int):
    return db.query(Genre).filter(Genre.id == genre_id).first()
