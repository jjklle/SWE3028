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
from fastapi import BackgroundTasks
import asyncio



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

def id_plus3000(id):
    return str(int(id)+2865-155)


def update_dataset(id, item_ls):
    path = './RecBole/dataset/contents/contents.inter'
    with open(path,'a') as f:
        for item in item_ls:
            f.write(str(id)+'\t'+str(item)+'\n')

def execute_recbole(user_id=2865):
    # 로그인 없이 처음 실행 시 default user id 2865로 실행
    # return type: dictionary 

    #recbole 실행
    os.chdir("./RecBole")
    os.system(f"python ./predict.py --user_id={user_id}")
    os.chdir("../")


def get_from_recommendls():
    os.chdir("./RecBole")
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
    webtoon = []

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
        if len(webtoon) < 8:
            if title[-1] == "w":
                webtoon.append((str(c),title[:-1]))

    os.chdir("../")

    return {'movie':movie,
            'drama':drama,
            'book':book,
            'webtoon':webtoon}

def train_recbole():
    os.chdir("./RecBole")
    os.system(f"python ./run_recbole.py --model=BPR --dataset=contents")
    os.chdir("../")


# @app.post('/recommend')
# async def get_recommendation(request: Request):
#     username = await request.json()
#     data = [1,2,3,4] # test

#     return data


@app.get('/register/preference')
def get_preference_form(request: Request):
    """
    Display preference page (only on registration)
    """
    return templates.TemplateResponse('preference.html', context={'request':request})


@app.post('/preference')
async def get_register_preference(request: Request, db:Session = Depends(get_db)):
    """
    Get data from preference page and train model
    """
    indices = await request.json()
    if len(indices)==0:
        indices=None
    username = request.cookies.get('username')

    _id = request.cookies.get('id')
    # print(username)
    # print(_id)
    user.put_preference(username,indices,db)
    #기존 데이터와 인덱스 충돌을 피하기 위해 3000을 더해서 사용
    update_dataset(id_plus3000(_id),indices) 
    train_recbole()
    execute_recbole(id_plus3000(_id))


@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})


@app.get("/mypage")
async def get_home(request: Request, db:Session = Depends(get_db)):
    username = request.cookies.get('username')
    preference_idx = user.get_preference(username, db) # index only

    preference = await content.get_multiple_contents(preference_idx, db) # list of content info

    return templates.TemplateResponse('mypage.html', context={'request':request, "preference":json.dumps(preference)})


@app.post("/recommend")
async def get_recommendation(request: Request):
    """
    Get user id from cookies, if logged in

    Cookies
    - access_token
    - id: index of user in db
    - username: user id
    - is_login: "True" or undefined
    """


    is_login = request.cookies.get('is_login')
    if(is_login=="True"):
        _id = request.cookies.get('id')
        print("id: ", _id)
        # execute_recbole(id_plus3000(_id))
        # execute_recbole(_id)
    else:
        execute_recbole()

    data = get_from_recommendls()
    # print(data)
    return json.dumps(data)

@app.post('/like')
async def update_like(request: Request, db:Session = Depends(get_db)):
    index = await request.json()
    username = request.cookies.get('username')
    user.update_preference(username,index['index'],db)
    

@app.get('/content/{index}')
async def get_content_page(request: Request, index: int, db: Session = Depends(get_db)):
    #유저 선호하는 리스트 가져와서, 현재 컨텐츠 페이지의 인덱스가 있는지 확인
    username = request.cookies.get('username')
    clicked=0
    if(username is not None):
        preference = user.get_preference(username, db)
        if preference != None and str(index) in preference:
            clicked=1
        else:
            clicked=0
    
    # get content from db
    category, content_info = await content.show_content(index, db)
    #print(content_info)
    #print(category, content_info)
    similar = await content.similar_content(index,db)
    
    if content_info is None:
        return templates.TemplateResponse('error.html', context={'request':request})
    
    if category=='m' or category=='t':
        # process strings
        content_info.genre = process_string_list(content_info.genre)
        content_info.casting = process_string_list(content_info.casting)
        content_info.platform = process_string_list(content_info.platform)

        return templates.TemplateResponse('content_movie.html', context={'request':request, 'content':content_info, 'category':category, 'index':index, 'similar':json.dumps(similar), 'like':clicked})
    
    elif category=='b':
        content_info.writer = process_string_list(content_info.writer)

        return templates.TemplateResponse('content_book.html', context={'request':request, 'content':content_info, 'category':category, 'index':index, 'similar':json.dumps(similar)})

    elif category=='w':
        # platform
        content_info.platform = process_string_list(content_info.platform)
        return templates.TemplateResponse('content_webtoon.html', context={'request':request, 'content':content_info, 'category':category, 'index':index, 'similar':json.dumps(similar)})

    else:
        return templates.TemplateResponse('error.html', context={'request':request})
    

@app.get('/search/')
async def search_content(request: Request, q: str, db: Session = Depends(get_db)):
    search_results = await search.search_content(q,db)

    return templates.TemplateResponse("search.html", {"request": request, "results": json.dumps(search_results), "query":q})


# @app.post("/train_recbole/")
# async def train(background_tasks: BackgroundTasks):
#     background_tasks.add_task(train_recbole())
#     return {"message": "success"}


