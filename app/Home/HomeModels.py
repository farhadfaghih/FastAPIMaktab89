from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from .Schema import Messages
from ..Core import models, dependencies
from datetime import datetime

BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db=Depends(dependencies.get_db)):
    recent_posts = db.query(models.Post).order_by(models.Post.id).limit(5).all()
    return templates.TemplateResponse("Home.html", {"request": request, "posts": recent_posts})


@router.get("/contact-us", response_class=HTMLResponse)
async def contactus(request: Request):
    return templates.TemplateResponse("Group2Maktab89 - Contact.html", {"request": request})


@router.post("/contact-us")
async def sendmessage(message: Messages, db=Depends(dependencies.get_db)) -> None:
    """
    Create a message for Superuser
    :param db: call database to store user messages
    :param message: message of user that comes from front-end. Must check with pydantic model to validate.
    :return: None
    """
    db_message = models.message(created_by=message.created_by, date_created=datetime.now(), email=message.email,
                                description=message.description)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return


@router.get("/about-us", response_class=HTMLResponse)
async def aboutus(request: Request):
    return templates.TemplateResponse("About.html", {"request": request})
