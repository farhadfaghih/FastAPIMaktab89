from fastapi import APIRouter, Request, Depends,File,UploadFile,Form
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
#pip install python-multipart.


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
async def create_a_new_post(file: UploadFile,title=Form(),body=Form(),db=Depends(get_db),user=Depends(get_user_from_cookie)) -> None:
    usr = db.query(User).filter(User.username == user["username"]).first()
    with open(f"static/{file.filename}","wb") as f:
       f.write(file.file.read())
    date = datetime.now()
    post = Post(title=title,body=body,image = f"static/{file.filename}",create_date = date.strftime("%m/%d/%Y, %H:%M:%S"),owner=usr)
    db.add(post)
    db.commit()
    db.refresh(post)
    return "success"
 

    
