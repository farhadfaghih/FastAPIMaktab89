from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="Template")
router = APIRouter(prefix="/posts")


@router.get("/{post_id}", response_class=HTMLResponse)
pass


@router.get("/allposts", response_class=HTMLResponse)
pass


