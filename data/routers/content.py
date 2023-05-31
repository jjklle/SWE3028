
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response
from database import engineconn
from db_class import MOVIE, TV, BOOK
from sqlalchemy.orm import Session
import json
router = APIRouter()

with open('contents_idx.json', 'r', encoding='UTF-8') as f:
    contents_idx = json.load(f)

def get_db():
    try:
        engine = engineconn()
        db = engine.sessionmaker()
        yield db
    finally:
        db.close()


@router.get("/{index}")
async def show_content(index: int, db: Session = Depends(get_db)):
    name = contents_idx[str(index)][:-1]
    cat = contents_idx[str(index)][-1]
    if cat == 'm':
        content = db.query(MOVIE).filter(MOVIE.name == name).first()
    elif cat == 't':
        content = db.query(TV).filter(TV.name == name).first()
    elif cat == 'b':
        content = db.query(BOOK).filter(BOOK.name == name).first()
    return content
