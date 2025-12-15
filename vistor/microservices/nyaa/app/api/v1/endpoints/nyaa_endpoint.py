from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.nyaa import create_nyaa, get_nyaa, update_nyaa, delete_nyaa
from app.schemas.nyaa import Nyaa, NyaaCreate
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Nyaa)
def create_nyaa(item: NyaaCreate, db: Session = Depends(get_db)):
    return create_nyaa(db=db, item=item)

@router.get("/{item_id}", response_model=Nyaa)
def read_nyaa(item_id: int, db: Session = Depends(get_db)):
    db_item = get_nyaa(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Nyaa not found")
    return db_item

@router.put("/{item_id}", response_model=Nyaa)
def update_nyaa(item_id: int, item: NyaaCreate, db: Session = Depends(get_db)):
    db_item = get_nyaa(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Nyaa not found")
    return update_nyaa(db=db, db_item=db_item, item=item)

@router.delete("/{item_id}", response_model=Nyaa)
def delete_nyaa(item_id: int, db: Session = Depends(get_db)):
    db_item = get_nyaa(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Nyaa not found")
    return delete_nyaa(db=db, item_id=item_id)

# Add more routes as needed
