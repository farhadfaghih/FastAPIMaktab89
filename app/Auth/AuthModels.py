from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import LoginRequest, RegisterNewUser
import sys
sys.path.append("..")
from app.Core.models import *
from app.Core.dependencies import *


BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})


@router.post("/login")
async def manage_user_login_request(login_request: LoginRequest, db=Depends(get_db)):
    user_check = db.query(User).filter(User.username == login_request.username).first()
    if user_check and user_check.password == login_request.password:
        return True
    else:
        raise HTTPException(status_code=404)


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
async def logout():
    pass
