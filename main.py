from fastapi import FastAPI, Path, HTTPException,Form, Request, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from starlette import status
from routers import user, content
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import json


app = FastAPI()
app.include_router(user.router)
app.include_router(content.router)

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


#recbole 실행
os.chdir("./RecBole")
user_id = 2865
os.system(f"python ./predict.py --user_id={user_id}")

with open('../contents_idx.json', 'r', encoding='UTF-8') as f:
    contents_idx = json.load(f)
# print(json.dumps(contents_idx,ensure_ascii = False))


f = open("./recommend_ls.txt", "r")
string = f.readline()
recommend_ls = list(map(int, string.split()))
contents = []
movie = []
tv = []
book = []


for content in recommend_ls:
    title = contents_idx[str(content)]
    if len(contents) < 8:
        contents.append(title[:-1])
    if len(movie) < 8:
        if title[-1] == "m":
            movie.append((str(content),title[:-1]))
    if len(tv) < 8:
        if title[-1] == "t":
            tv.append(title[:-1])
    if len(book) < 8:
        if title[-1] == "b":
            book.append(title[:-1])

#print(contents)
#print(movie)
#print(tv)
#print(book)
os.chdir("../")

# @app.get('/login')
# def get_login_form(request: Request):
#     return templates.TemplateResponse('login.html', context={'request':request})

# @app.get('/register')
# def get_register_form(request: Request):
#     return templates.TemplateResponse('register.html', context={'request':request})

@app.post('/recommend')
async def get_recommendation(request: Request):
    username = await request.json()
    data = [1,2,3,4] # test

    return data


@app.get('/register/preference')
def get_preference_form(request: Request):
    return templates.TemplateResponse('preference.html', context={'request':request})

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request, 'movie':movie, 'tv':tv, 'book':book})

