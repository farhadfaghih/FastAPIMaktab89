from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="Template")
router = APIRouter(prefix="/superuser")


@router.get("/dashboard", response_class=HTMLResponse)
pass


@router.get("/posts", response_class=HTMLResponse)
pass

@router.get("/comments", response_class=HTMLResponse)
pass

@router.get("/messages", response_class=HTMLResponse)
pass
