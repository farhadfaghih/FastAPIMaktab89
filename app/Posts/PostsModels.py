from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.Core.models import *
from app.Core.dependencies import *
from pathlib import Path
from app.Auth.AuthModels import get_user_from_cookie
from .Schema import Comments

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/post/{id}", response_class=HTMLResponse)
async def detail_post(id, request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    user_exist = user["usertype"]
    if user_exist:
        user_exist = db.query(User.fullname).filter(User.username == user["username"]).first()
    post = db.query(Post).filter(Post.id == id).first()
    return templates.TemplateResponse("Post_with_detail.html",
                                      {"request": request, "post": post, "usertype": user_exist})


@router.post("/post")
async def comment(user_comment: Comments, db=Depends(get_db), user=Depends(get_user_from_cookie)) -> None:
    """
    Create a comment for a post
    :param user: check Login condition first
    :param db: call database to store user comments
    :param user_comment: User Comment on a post that comes from front-end. Must check with pydantic model to validate.
    :return: None
    """
    user_requesting = db.query(User.fullname).filter(User.username == user["username"]).first()
    db_comment = Comment(description=user_comment.description, date_created=datetime.now().strftime("%b %d, %Y"),
                         owner_id=user_requesting, post_id=user_comment.post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return


@router.get("/allposts/", response_class=HTMLResponse)
async def all_posts(request: Request, db=Depends(get_db)):
    allposts = db.query(Post.id, Post.image, Post.title, Post.body, Post.create_date, Post.owner_id,
                        User.fullname).join(User, Post.owner_id == User.id).all()
    return templates.TemplateResponse("Posts.html", {"request": request, "posts": allposts})
