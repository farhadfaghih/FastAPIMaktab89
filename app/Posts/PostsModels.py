from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..Core import models, dependencies

templates = Jinja2Templates(directory="Template")
router = APIRouter(prefix="/posts")


@router.get("/{post_id}", response_class=HTMLResponse)
async def detail_post(id, request: Request, db=Depends(dependencies.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/allposts", response_class=HTMLResponse)
async def all_posts(request: Request, db=Depends(dependencies.get_db)):
    posts = db.query(models.Post).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})