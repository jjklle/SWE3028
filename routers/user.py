import sys
sys.path.append('..')

from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from pydantic import BaseModel
from database import engineconn
from db_class import User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt,JWTError
from jose.exceptions import ExpiredSignatureError

router = APIRouter()
"""
engine = engineconn()
session = engine.sessionmaker()
"""
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")

ALGORITHM = 'HS256'
TOKEN_EXPIRE_MIN = 30
REFRESH_TOKEN_EXPIRE_MIN = 60 * 24 * 7
SECRET_KEY = "SECRET_KEY"
REFRESH_SECRET_KEY="REFRESH_SECRET_KEY"

class LoginInput(BaseModel):
    username:str
    password:str

class check_id(BaseModel):
    id:str

class CreateUser(BaseModel):
    username: str
    password: str
    email: str
    

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_db():
    try:
        engine = engineconn()
        db = engine.sessionmaker()
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.user_id == username).first()
    try:
        result = bcrypt_context.verify(password, user.password)
        if user and result:
            return user
        else:
            return False
    except:
        return False


def create_access_token(username: str, expires_delta: int = None)-> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes = TOKEN_EXPIRE_MIN)
    
    encode = {"exp": expires_delta, "sub": username}
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

def create_refresh_token(username: str, expires_delta: int = None)-> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes = REFRESH_TOKEN_EXPIRE_MIN)
    
    encode = {"exp": expires_delta, "sub": username}
    return jwt.encode(encode, REFRESH_SECRET_KEY, ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not find user",
        )
        return {"id": username}
    
    except ExpiredSignatureError:
        raise HTTPException(
        status_code=403,
        detail="Token has been expired",
        )
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        )
    
@router.post('/login',status_code=200)
def login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)

    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )
    else:
        expire = timedelta(minutes=TOKEN_EXPIRE_MIN)
        token = create_access_token(form_data.username, expire)
        return {"id":user.id, "token": token} # return user index in the db and token
    
"""
@router.post('/register/check',status_code=200)
def check(input: check_id):
    result = session.query(User).filter_by(user_id=input.id).first()
    if result != None:
        return {"exists":"1"}
    else:
        return 1
"""
@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(username: str = Form(...), password: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    
    result = db.query(User).filter_by(user_id=username).first()
    if result != None: #이미 있는 계정
        raise HTTPException(
        status_code=409,
        detail="username already exists"
    )
    
    else:
        hash_password = bcrypt_context.hash(password)
        new_user = User(username , hash_password , email)
        db.add(new_user)
        db.commit()
        # return access token
        expire = timedelta(minutes=TOKEN_EXPIRE_MIN)
        token = create_access_token(username, expire)
        return {"token": token}
    