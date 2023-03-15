from fastapi import APIRouter, Request, Depends, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from pathlib import Path
from .Schema import NewPost, PostID
import sys
sys.path.append("..")
from app.Core.dependencies import *
from app.Core.models import *
from app.Auth.AuthModels import get_user_from_cookie
#pip install python-multipart.


BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/admin")


@router.get("/dashboard")
async def all_posts(request: Request, db=Depends(get_db), user=Depends(get_user_from_cookie)):
    if user["usertype"] != "normal":
        usr = db.query(User).filter(User.username == user["username"]).first()
        allposts = usr.posts
        return templates.TemplateResponse("Admin_dashboard.html", {"request": request, "allposts": allposts})
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to access this page.")


@router.post("/dashboard")
async def create_a_new_post(file: UploadFile,title=Form(),body=Form(),db=Depends(get_db),user=Depends(get_user_from_cookie)) -> None:
    usr = db.query(User).filter(User.username == user["username"]).first()
    with open(f"static/{file.filename}","wb") as f:
       f.write(file.file.read())
    date = datetime.now()
    post = Post(title=title,body=body,image = f"static/{file.filename}",create_date = date.strftime("%m/%d/%Y, %H:%M:%S"),owner=usr)
    db.add(post)
    db.commit()
    return "success"



@router.delete("/dashboard")
async def delete_a_post(post_id: PostID, db=Depends(get_db)) -> None:
    db_delete_post = db.query(Post).filter(Post.id == post_id.id).first()
    db.delete(db_delete_post)
    db.commit()
    db.refresh(db_delete_post)
    return "success"
