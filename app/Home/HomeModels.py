from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import Messages
from app.Core.models import *
from app.Core.dependencies import *
from datetime import datetime

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db=Depends(get_db)):
    recent_posts = db.query(Post.id, Post.image, Post.title, Post.body, Post.create_date, Post.owner_id,
                            User.fullname).join(User, Post.owner_id == User.id).order_by(Post.id).limit(3).all()
    return templates.TemplateResponse("Home.html", {"request": request, "posts": recent_posts})


@router.get("/contact-us", response_class=HTMLResponse)
async def contactus(request: Request):
    return templates.TemplateResponse("Contact.html", {"request": request})


@router.post("/contact-us")
async def sendmessage(messages: Messages, db=Depends(get_db)) -> None:
    """
    Create a message for Superuser
    :param db: call database to store user messages
    :param messages: message of user that comes from front-end. Must check with pydantic model to validate.
    :return: None
    """
    db_message = message(created_by=messages.created_by, date_created=datetime.now().strftime("%b %d, %Y"),
                         email=messages.email, description=messages.description)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return


@router.get("/about-us", response_class=HTMLResponse)
async def aboutus(request: Request):
    return templates.TemplateResponse("About.html", {"request": request})
