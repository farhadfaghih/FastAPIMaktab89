from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="Template")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/contact-us", response_class=HTMLResponse)
async def contactus(request: Request):
    return templates.TemplateResponse("contactus.html", {"request": request})


@router.get("/about-us", response_class=HTMLResponse)
async def aboutus(request: Request):
    return templates.TemplateResponse("aboutus.html", {"request": request})