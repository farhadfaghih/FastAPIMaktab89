from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import LoginRequest
from..Core import models, dependencies


BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})


@router.post("/login")
async def manage_user_login_request(login_request: LoginRequest, db=Depends(dependencies.get_db)):
    user_check = db.query(models.User).filter(models.User.username == login_request.username).first()
    if user_check and user_check.password == login_request.password:
        return True
    else:
        raise HTTPException(status_code=404)


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("Register.html", {"request": request})

