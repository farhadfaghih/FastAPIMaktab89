from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import sys
from .Schema import ModifyContent

sys.path.append("..")
from app.Core.dependencies import *
from app.Core.models import *

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/superuser")


@router.get("/dashboard", response_class=HTMLResponse)
async def superuser_dashboard(request: Request, db=Depends(get_db)):
    messages = db.query(message).all()
    comments = db.query(Comment.id, Comment.description, Comment.date_created, Comment.confirmed, Comment.post_id,
                        User.fullname, Post.title).join(User, Comment.owner_id == User.id).join(Post,
                        Comment.post_id == Post.id).filter(Comment.confirmed == False).all()
    posts = db.query(Post).all()
    return templates.TemplateResponse("Superuser_dashboard.html",
                                      {"request": request, "messages": messages, "comments": comments, "posts": posts})


@router.delete("/messages")
async def delete_a_message(message_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_message = db.query(message).filter(message.id == message_id.id).first()
    db.delete(db_delete_message)
    db.commit()


@router.delete("/comments")
async def delete_a_message(comment_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_comment = db.query(Comment).filter(Comment.id == comment_id.id).first()
    db.delete(db_delete_comment)
    db.commit()


@router.patch("/comments")
async def approve_a_message(comment_id: ModifyContent, db=Depends(get_db)) -> None:
    db_comment = db.query(Comment).filter(Comment.id == comment_id.id).first()
    db_comment.confirmed = True
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)


@router.delete("/posts")
async def delete_a_post(post_id: ModifyContent, db=Depends(get_db)) -> None:
    db_delete_post = db.query(Post).filter(Post.id == post_id.id).first()
    db.delete(db_delete_post)
    db.commit()
