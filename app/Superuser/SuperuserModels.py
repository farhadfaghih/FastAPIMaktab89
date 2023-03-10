from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH / "Templates"))
router = APIRouter(prefix="/superuser")


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("Superuser_dashboard.html", {"request": request})
#
# @router.get("/posts", response_class=HTMLResponse)
# pass
#
# @router.get("/comments", response_class=HTMLResponse)
# pass
#
# @router.get("/messages", response_class=HTMLResponse)
# pass
