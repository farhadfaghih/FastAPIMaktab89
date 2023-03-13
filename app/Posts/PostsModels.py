from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.Core.models import *
from app.Core.dependencies import *

templates = Jinja2Templates(directory="Template")
router = APIRouter(prefix="/posts")


@router.get("/{post_id}", response_class=HTMLResponse)
async def detail_post(id, request: Request, db=Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/allposts", response_class=HTMLResponse)
async def all_posts(request: Request, db=Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})