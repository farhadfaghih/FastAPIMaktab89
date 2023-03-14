from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.Core.models import *
from app.Core.dependencies import *
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/posts")


@router.get("/{post_id}", response_class=HTMLResponse)
async def detail_post(id, request: Request, db=Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return templates.TemplateResponse("Post_with_detail.html", {"request": request, "post": post})


@router.get("/allposts", response_class=HTMLResponse)
async def all_posts(request: Request, db=Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("Posts.html", {"request": request, "posts": posts})