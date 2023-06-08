
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response
from database import engineconn
from db_class import MOVIE, TV, BOOK, WEBTOON
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


async def show_content(index: int, db:Session = Depends(get_db)):
    """
    return: category(m,t,b,w), content info (depends on db schema)
    """

    name = contents_idx[str(index)][:-1]
    cat = contents_idx[str(index)][-1]
    print(cat== 'w')
    try:
        if cat == 'm':
            content = db.query(MOVIE).filter(MOVIE.name == name).first()
            
        elif cat == 't':
            content = db.query(TV).filter(TV.name == name).first()
        elif cat == 'b':
            content = db.query(BOOK).filter(BOOK.name == name).first()
        elif cat == 'w':
            content = db.query(WEBTOON).filter(WEBTOON.name == name).first()
    except Exception as e :
        #print(e)
        content=None
    return cat, content


async def similar_content(index: int, db:Session = Depends(get_db)):
    """
    Args:
        index: integer index of a content 

    Return: 
        list of contents (index, category, content name)
    """
    with open('./routers/indices.txt','rb') as f:
        indices = f.readlines()
    output = indices[index-1].decode('UTF-8').split()[1:]
    output = [int(elem)+1 for elem in output]
    # print(output)
    result = []
    for idx in output[:5]:
        cat, item = await show_content(idx, db)
        if(item is not None):
            result.append([idx, cat, item.name])

    return result


async def get_multiple_contents(idx_list, db:Session = Depends(get_db)):
    """
    Get information of multiple contents at once

    return: 
        list of contents (index, category, content name)
    """
    result = []
    for idx in idx_list:
        cat, item = await show_content(idx, db)
        if(item is not None):
            result.append([idx, cat, item.name])
    
    return result
