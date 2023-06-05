from fastapi import Depends, HTTPException, status, APIRouter, Request, Response
from database import engineconn
from db_class import MOVIE, TV, BOOK
from sqlalchemy import func
from sqlalchemy.orm import Session
from fuzzywuzzy import fuzz
import re
import json
router = APIRouter()


with open('contents_idx.json', 'r', encoding='UTF-8') as f:
    contents_idx = json.load(f)

result=[]
punctuation = '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\s]'

def get_db():
    try:
        engine = engineconn()
        db = engine.sessionmaker()
        yield db
    finally:
        db.close()

def name_to_index(content_name):
    for k, v in contents_idx.items():
        if v[:-1] == content_name:
            return k, v[-1]
    return None,None

def tuple_to_list(t):
    idx, cat = name_to_index(t[0])
    if not idx:
        return 1
    tu = [idx, cat] + list(t)
    tu = tuple(tu)
    if tu in result:
        return 1
    result.append(tu)

def search_movie_name(query, db):
    query = re.sub(punctuation,"",query)
    query = "%" + query +"%"
    sub_result = db.query(MOVIE.name, MOVIE.director, MOVIE.casting,MOVIE.country, MOVIE.year, MOVIE.description).filter(func.regexp_replace(MOVIE.name, punctuation,"").ilike(query)).all()
    for t in sub_result:
        tuple_to_list(t)

    
def search_tv_name(query, db):
    query = re.sub(punctuation,"",query)
    query = "%" + query +"%"
    sub_result = db.query(TV.name, TV.director, TV.casting,TV.country, TV.year, TV.description).filter(func.regexp_replace(TV.name, punctuation,"").ilike(query)).all()
    for t in sub_result:
        tuple_to_list(t)

def search_book_name(query, db):
    query = re.sub(punctuation,"",query)
    query = "%" + query +"%"
    sub_result = db.query(BOOK.name, BOOK.writer, BOOK.author,  BOOK.year, BOOK.description).filter(func.regexp_replace(BOOK.name, punctuation,"").ilike(query)).all()
    for t in sub_result:
        tuple_to_list(t)
    

"""
def search_description(query, db):
    keywords = query.split()
    query = re.sub(punctuation,"",keywords[0])
    query = "%" + query +"%"
    sub_result = db.query(MOVIE.name, MOVIE.director, MOVIE.casting,MOVIE.country, MOVIE.year, MOVIE.description).filter(func.regexp_replace(MOVIE.description, punctuation,"").ilike(query))
    print(sub_result.all())
    if len(sub_result.all())==0 or len(keywords)==1 :
        tuple_to_list(sub_result.all())
        return 1

    for idx in range(1,len(keywords)):
        query = re.sub(punctuation,"",keywords[idx])
        query = "%" + query +"%"
        sub_result = sub_result.filter(func.regexp_replace(MOVIE.description, punctuation,"").ilike(query))
    tuple_to_list(sub_result.all())

"""
def search_movie_people(query, db):
    names = query.split()
    res = db.query(MOVIE.name, MOVIE.director, MOVIE.casting, MOVIE.country, MOVIE.year, MOVIE.description).all()
    for i in res:
        people = re.sub("[,\']","",i[2][1:-1])
        people=people.split(' ')
        people.append(i[1])
        present = all(elem in people for elem in names)
        
        if present:
            tuple_to_list(i)

def search_tv_people(query, db):
    names = query.split()
    res = db.query(TV.name, TV.director, TV.casting, TV.country, TV.year, TV.description).all()
    for i in res:
        people = re.sub("[,\']","",i[2][1:-1])
        people=people.split(' ')
        people.append(i[1])
        present = all(elem in people for elem in names)
        
        if present:
            tuple_to_list(i)            

def search_book_people(query, db):
    names = query.split()
    res = db.query(BOOK.name, BOOK.writer, BOOK.author,  BOOK.year, BOOK.description).all()

    for i in res:
        people = re.sub("[,\']","",i[1][1:-1])
        people=people.split(' ')
        wi = i[2].split('/')
        people = people + wi
        present = all(elem in people for elem in names)
        
        if present:
            tuple_to_list(i) 

"""
def search_people(query,db):
    names = query.split()
    query = re.sub(punctuation,"",names[0])
    query = "%" + query +"%"
    sub_result = db.query(MOVIE.name, MOVIE.MOVIE.director, MOVIE.casting).filter(func.regexp_replace(MOVIE.casting, punctuation,"").ilike(query)|func.regexp_replace(MOVIE.director, punctuation,"").ilike(query))
    if len(sub_result.all())==0 or len(names)==1 :
        tuple_to_list(sub_result.all())
        return 1
    
    for idx in range(1,len(names)):
        query = re.sub(punctuation,"",names[idx])
        query = "%" + query +"%"
        sub_result = sub_result.filter(func.regexp_replace(MOVIE.casting, punctuation,"").ilike(query)|func.regexp_replace(MOVIE.director, punctuation,"").ilike(query))
    
    tuple_to_list(sub_result.all())
"""

async def search_content(q: str, db: Session = Depends(get_db)):
    result.clear()
    names = q.split()
    #description 함수 추가를 통해, 요약 정보에 검색하는 키워드가 있는지 나타낼 수 있지만, 결과를 도출하는 데 시간이 너무 많이 걸립니다.
    """
    return: list of arrays
        each array contains:
        id, category, title, director(author), ...
    """
    search_movie_name(q,db)
    
    if len(names)>1:
        search_movie_name(names[0],db)
    
    search_movie_people(q,db)


    search_tv_name(q,db)
    
    if len(names)>1:
        search_tv_name(names[0],db)
    
    search_tv_people(q,db)


    search_book_name(q,db)
    
    if len(names)>1:
        search_book_name(names[0],db)
    
    search_book_people(q,db)

    return result
    


