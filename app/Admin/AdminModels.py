from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="Template")
router = APIRouter(prefix="/admin")


# @router.get("/dashboard", response_class=HTMLResponse)
# pass



