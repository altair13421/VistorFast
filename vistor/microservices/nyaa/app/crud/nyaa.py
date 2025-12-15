from sqlalchemy.orm import Session
from app.models.nyaa import *
from app.schemas.nyaa import *

def get_nyaa(db: Session, item_id: int):
    return db.query(Nyaa).filter(Nyaa.id == item_id).first()

def create_nyaa(db: Session, item: NyaaCreate):
    db_item = Nyaa(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_nyaa(db: Session, db_item: Nyaa, item: NyaaCreate):
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_nyaa(db: Session, item_id: int):
    db_item = db.query(Nyaa).filter(Nyaa.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item
