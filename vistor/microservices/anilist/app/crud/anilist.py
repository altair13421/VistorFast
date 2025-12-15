from sqlalchemy.orm import Session
from app.models.anilist import *
from app.schemas.anilist import *

def get_anilist(db: Session, item_id: int):
    return db.query(Anilist).filter(Anilist.id == item_id).first()

def create_anilist(db: Session, item: AnilistCreate):
    db_item = Anilist(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_anilist(db: Session, db_item: Anilist, item: AnilistCreate):
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_anilist(db: Session, item_id: int):
    db_item = db.query(Anilist).filter(Anilist.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item
