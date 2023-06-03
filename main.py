from fastapi import FastAPI, Path, HTTPException,Form, Request, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from starlette import status
from routers import user, content, search#google
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import json
from sqlalchemy.orm import Session
from database import engineconn
from sqlalchemy.orm import Session
from utils import *



def get_db():
    try:
        engine = engineconn()
        db = engine.sessionmaker()
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(user.router)
app.include_router(content.router)
#app.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

def execute_recbole(user_id=2864):
    # 로그인 없이 처음 실행 시 default user id 2865로 실행
    # return type: dictionary 

    #recbole 실행
    os.chdir("./RecBole")
    os.system(f"python ./predict.py --user_id={user_id}")


def get_from_recommendls():
    with open('../contents_idx.json', 'r', encoding='UTF-8') as _f:
        contents_idx = json.load(_f)
    # print(json.dumps(contents_idx,ensure_ascii = False))

    f = open("./recommend_ls.txt", "r")
    string = f.readline()
    recommend_ls = list(map(int, string.split()))
    contents = []
    movie = []
    drama = []
    book = []

    for c in recommend_ls:
        title = contents_idx[str(c)]
        if len(contents) < 8:
            contents.append(title[:-1])
        if len(movie) < 8:
            if title[-1] == "m":
                movie.append((str(c),title[:-1]))
        if len(drama) < 8:
            if title[-1] == "t":
                drama.append((str(c),title[:-1]))
        if len(book) < 8:
            if title[-1] == "b":
                book.append((str(c),title[:-1]))

    os.chdir("../")

    return {'movie':movie,
            'drama':drama,
            'book':book}


# @app.post('/recommend')
# async def get_recommendation(request: Request):
#     username = await request.json()
#     data = [1,2,3,4] # test

#     return data


@app.get('/register/preference')
def get_preference_form(request: Request):
    return templates.TemplateResponse('preference.html', context={'request':request})

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})



@app.post("/recommend")
async def get_recommendation(request: Request):
    """
    Get user id from cookies, if logged in

    Cookies
    - access_token
    - id: index of user in db
    - username: user id
    - is_login
    """
    # need to fix

    # is_login = request.cookies.get('is_login')
    # if(is_login=="True"):
    #     _id = request.cookies.get('id')
    #     data = execute_recbole(_id)
    # else:
    #     data = execute_recbole()
    execute_recbole()
    data = get_from_recommendls()
    # print(data)
    return json.dumps(data)


@app.get('/content/{index}')
async def get_content_page(request: Request, index: int, db: Session = Depends(get_db)):
    
    
    # get content from db
    category, content_info = await content.show_content(index, db)
    similar = await content.similar_content(index,db) #유사한 컨텐츠 인덱스입니다
    if content_info is None:
        return templates.TemplateResponse('error.html', context={'request':request})
    
    if category=='m' or category=='t':
        # process strings
        content_info.genre = process_string_list(content_info.genre)
        content_info.casting = process_string_list(content_info.casting)
        content_info.platform = process_string_list(content_info.platform)

        return templates.TemplateResponse('content_movie.html', context={'request':request, 'content':content_info, 'category':category})
    
    elif category=='b':
        content_info.writer = process_string_list(content_info.writer)

        return templates.TemplateResponse('content_book.html', context={'request':request, 'content':content_info, 'category':category})

    else:
        return templates.TemplateResponse('error.html', context={'request':request})
    

@app.get('/search/')
async def search_content(request: Request, q: str, db: Session = Depends(get_db)):
    result = await search.search_content(q,db)
    return result

