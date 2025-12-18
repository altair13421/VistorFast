from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.nyaa import create_nyaa, get_nyaa, update_nyaa, delete_nyaa
from app.schemas.nyaa import Nyaa, NyaaCreate
from app.db.session import get_db
from app.utils.search import query_nyaa

router = APIRouter()

@router.get("/search", response_model=Nyaa)
def search_nyaa(
    item: NyaaCreate, db: Session = Depends(get_db),
    search:str = "", # search query
    page:int = 1, # page number
    c:str = "0_0", # category
):
    return query_nyaa(db=db, item=item)

@router.get("/categories")
def get_categories():
    from app.core.config import settings
    return settings.categories
