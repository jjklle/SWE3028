from fastapi import FastAPI, Depends, Path, HTTPException,Form, Request
from pydantic import BaseModel
from database import engineconn
from db_class import User
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from starlette import status

app = FastAPI()

engine = engineconn()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static") 
session = engine.sessionmaker()

class login_input(BaseModel):
    username:str
    password:str

class check_id(BaseModel):
    id:str

class register_input(BaseModel):
    id : str
    password : str
    email : str


@app.get('/login')
def get_login_form(request: Request):
    return templates.TemplateResponse('login.html', context={'request':request})

@app.post('/token',status_code=200)
def login(input: login_input):
    result = session.query(User).filter_by(user_id=input.username).first()
    if result and result.password == input.password :
        return 1    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    

@app.get('/register')
def get_login_form(request: Request):
    return templates.TemplateResponse('register.html', context={'request':request})

@app.post('/register/check',status_code=200)
def check(input: check_id):
    result = session.query(User).filter_by(user_id=input.id).first()
    if result != None:
        return {"exists":"1"}
    else:
        return 1

@app.post('/register/registration', status_code=200)
def register(input: register_input):
    new_user = User(input.id,input.password,input.email)
    result = session.add(new_user)
    session.commit()
    return 1


@app.get("/index.html")
async def get_home(request: Request):
    return templates.TemplateResponse('index.html', context={'request':request})
