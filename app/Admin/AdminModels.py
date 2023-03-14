from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import NewPost
import sys
sys.path.append("..")
from app.Core.dependencies import *
from app.Core.models import *
from datetime import datetime
from app.Auth.AuthModels import get_user_from_cookie

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/admin")


@router.get("/dashboard")
async def all_posts(request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    if user["usertype"] != "admin":
        return "False"
    usr = db.query(User).filter(User.username == user["username"]).first()
    allposts = usr.posts
    return templates.TemplateResponse("Admin_dashboard.html", {"request": request, "allposts": allposts})


@router.post("/dashboard")
async def create_a_new_post(new_post: NewPost, db=Depends(get_db)) -> None:
    db_new_post = Post(image=new_post.image, title=new_post.title, body=new_post.body,
                       created_date=datetime.now().strftime("%b %d, %Y"))
    db.add(db_new_post)
    db.commit()
    db.refresh(db_new_post)
    return
