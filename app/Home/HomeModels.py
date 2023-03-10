from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("Home.html", {"request": request})


@router.get("/contact-us", response_class=HTMLResponse)
async def contactus(request: Request):
    return templates.TemplateResponse("Contact.html", {"request": request})


@router.get("/about-us", response_class=HTMLResponse)
async def aboutus(request: Request):
    return templates.TemplateResponse("About.html", {"request": request})
