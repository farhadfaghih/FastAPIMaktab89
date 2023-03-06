from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="Template")
router = APIRouter(prefix="/auth")


@router.get("/login", response_class=HTMLResponse)
pass


@router.get("/register", response_class=HTMLResponse)
pass


