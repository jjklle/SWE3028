from fastapi import FastAPI, Depends, Path, HTTPException,Form, Request
from pydantic import BaseModel
from database import engineconn
from db_class import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from starlette import status
from routers import user
app = FastAPI()
app.include_router(user.router)

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static") 

@app.get('/login')
def get_login_form(request: Request):
    return templates.TemplateResponse('login.html', context={'request':request})

# @app.get('/register')
# def get_register_form(request: Request):
#     return templates.TemplateResponse('register.html', context={'request':request})

@app.get('/register/preference')
def get_preference_form(request: Request):
    return templates.TemplateResponse('preference.html', context={'request':request})

@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})

