from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.anilist import *
from app.schemas.anilist import *
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Anilist)
def create_anilist(item: AnilistCreate, db: Session = Depends(get_db)):
    return create_anilist(db=db, item=item)

@router.get("/{item_id}", response_model=Anilist)
def read_anilist(item_id: int, db: Session = Depends(get_db)):
    db_item = get_anilist(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Anilist not found")
    return db_item

@router.put("/{item_id}", response_model=Anilist)
def update_anilist(item_id: int, item: AnilistCreate, db: Session = Depends(get_db)):
    db_item = get_anilist(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Anilist not found")
    return update_anilist(db=db, db_item=db_item, item=item)

@router.delete("/{item_id}", response_model=Anilist)
def delete_anilist(item_id: int, db: Session = Depends(get_db)):
    db_item = get_anilist(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Anilist not found")
    return delete_anilist(db=db, item_id=item_id)

# Add more routes as needed
