from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.music import *
from app.schemas.music import *
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Music)
def create_music(item: MusicCreate, db: Session = Depends(get_db)):
    return create_music(db=db, item=item)

@router.get("/{item_id}", response_model=Music)
def read_music(item_id: int, db: Session = Depends(get_db)):
    db_item = get_music(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return db_item

@router.put("/{item_id}", response_model=Music)
def update_music(item_id: int, item: MusicCreate, db: Session = Depends(get_db)):
    db_item = get_music(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return update_music(db=db, db_item=db_item, item=item)

@router.delete("/{item_id}", response_model=Music)
def delete_music(item_id: int, db: Session = Depends(get_db)):
    db_item = get_music(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Music not found")
    return delete_music(db=db, item_id=item_id)

# Add more routes as needed
