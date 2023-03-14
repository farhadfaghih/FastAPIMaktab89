from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from Schema import NewPost
from app.Core.dependencies import *
from app.Core.models import *
from datetime import datetime

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/admin")


@router.get("/dashboard", response_class=HTMLResponse)
async def all_posts(request: Request, db=Depends(get_db)):
    allposts = db.query(Post.id, Post.image, Post.title, Post.body, Post.create_date, Post.owner_id,
                        User.fullname).join(User, Post.owner_id == User.id).all()
    return templates.TemplateResponse("Admin_dashboard.html", {"request": request, "posts": allposts})


@router.post("/dashboard")
async def create_a_new_post(new_post: NewPost, db=Depends(get_db)) -> None:
    db_new_post = Post(image=new_post.image, title=new_post.title, body=new_post.body,
                       created_date=datetime.now().strftime("%b %d, %Y"))
    db.add(db_new_post)
    db.commit()
    db.refresh(db_new_post)
    return
