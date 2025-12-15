from sqlalchemy.orm import Session
from app.models.music import *
from app.schemas.music import *

def get_music(db: Session, item_id: int):
    return db.query(Music).filter(Music.id == item_id).first()

def create_music(db: Session, item: MusicCreate):
    db_item = Music(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_music(db: Session, db_item: Music, item: MusicCreate):
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_music(db: Session, item_id: int):
    db_item = db.query(Music).filter(Music.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item
