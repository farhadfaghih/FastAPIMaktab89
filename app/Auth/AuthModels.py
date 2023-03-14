from fastapi import Depends, APIRouter, Request, HTTPException, Response,status,Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import LoginRequest, RegisterNewUser
import sys
sys.path.append("..")
from app.Core.models import *
from app.Core.dependencies import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from pydantic import BaseModel

#pip install "python-jose[cryptography]"
#pip install "passlib[bcrypt]"

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563h93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



############################################################################################################################################################################
class Token(BaseModel):
    access_token: str
    token_type: str

def get_user_from_cookie(req):
    token = req.cookies.get("token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        usertype :str = payload.get("usertype")
        print(payload.get("usertype"))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username":username,"usertype":usertype}
    

def authenticate_user( username: str, password: str,db):
    user_check = db.query(User).filter(User.username == username).first()
    if user_check:
        return user_check
    else:
        raise HTTPException(status_code=404)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@router.post("/login",response_model=Token)
async def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends(),db = Depends(get_db)):
    user = authenticate_user( form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_admin :
        usertype = "admin"
    elif user.is_superuser:
        usertype = "superuser"
    else : 
        usertype = "normal"
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username,"usertype":usertype}, expires_delta=access_token_expires
    )
    response.set_cookie(key="token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/")
async def read_users_me(request: Request):
    
    user = get_user_from_cookie(request)
    return user


###########################################################################################################################################################################



@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})


# @router.post("/login")
# async def manage_user_login_request(login_request: LoginRequest, db=Depends(get_db)):
#     user_check = db.query(User).filter(User.username == login_request.username).first()
#     if user_check and user_check.password == login_request.password:
#         return True
#     else:
#         raise HTTPException(status_code=404)


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("Register.html", {"request": request})


@router.post("/register")
async def manage_user_register_request(newuser: RegisterNewUser, db=Depends(get_db)):
    db_user = User(fullname=newuser.fullname, username=newuser.username, email=newuser.email
                          , password=newuser.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return



    
@router.get("/logout")
def logout(response:Response):
    response.set_cookie(key="token", value="")