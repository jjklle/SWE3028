from fastapi import FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

app = FastAPI()

# Mock Database
users_db = []

# OAuth2PasswordBearer for handling authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model for registration
class UserRegister(BaseModel):
    username: str
    password: str

# User model for login
class UserLogin(BaseModel):
    username: str
    password: str

templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("./login.html",{"request": request})

# Route to register a new user
@app.post("/register")
def register(user: UserRegister):
    # Check if username already exists
    
    for u in users_db:
        if u['username'] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    # Create a new user
    new_user = {'username': user.username, 'password': user.password}
    users_db.append(new_user)
    return {"message": "User registered successfully"}

# Route to login and get a token
@app.post("/token")
def login(user: UserLogin):
    # Check if username and password match
    for u in users_db:
        if u['username'] == user.username and u['password'] == user.password:
            # Return a token
            return {"token": user.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected route that requires authentication
# @app.get("/protected")
# def protected_route(token: str = Depends(oauth2_scheme)):
#     # Check if token exists in users_db
#     for u in users_db:
#         if u['username'] == token:
#             return {"message": "Access granted"}
#     raise HTTPException(status_code=401, detail="Invalid token")