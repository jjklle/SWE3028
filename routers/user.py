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
import os
import threading

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

"""
선호도 처리하는 함수들
"""
def get_preference(username:str, db):
    user = db.query(User).filter(User.user_id == username).first()
    if user.preference == None:
        preference=None
    else:
        preference= user.preference.split(', ')
    print(preference)
    return preference



def put_preference(username:str, preference: list, db):
    if preference==None:
        updated_preference=None
    else:
        updated_preference = ", ".join(preference)
    user = db.query(User).filter(User.user_id == username).update({'preference': updated_preference})
    db.commit()



def update_preference(username:str, index:str, db):
    preference = get_preference(username,db)
    if preference==None:
        updated_preference=index
    elif index in preference:
        if len(preference)==1:
            updated_preference=None
        else:
            preference.remove(index)
            updated_preference = ", ".join(preference)
    else:
        preference.append(index)
        updated_preference = ", ".join(preference)

    db.query(User).filter(User.user_id == username).update({'preference': updated_preference})
    db.commit()




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


def execute_recbole(user_id=2865):
    # 로그인 없이 처음 실행 시 default user id 2865로 실행
    # return type: dictionary 

    #recbole 실행
    os.chdir("./RecBole")
    os.system(f"python ./predict.py --user_id={user_id}")
    os.chdir("../")

def id_plus3000(id):
    return str(int(id)+2865-155)


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
        execute_recbole(id_plus3000(user.id))
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
        # need to find the generated id and return with token
        user = db.query(User).filter_by(user_id=username).first()
        expire = timedelta(minutes=TOKEN_EXPIRE_MIN)
        token = create_access_token(username, expire)
        return {"id": user.id, "token": token}
    

@router.delete("/user/{username}")
async def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(user_id=username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "회원 탈퇴가 완료되었습니다."}
