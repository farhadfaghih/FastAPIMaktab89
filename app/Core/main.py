from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
import models
import dependencies
from database import engine

from ..Admin import Models
from ..Auth import Models
from ..Home import Models
from ..Posts import Models
from ..Superuser import Models


models.Base.metadata.create_all(bind=engine)
app = FastAPI(dependencies=[Depends(dependencies.get_db)])

app.include_router(app.Admin.Models.router)
app.include_router(app.Auth.Models.router)
app.include_router(app.Home.Models.router)
app.include_router(app.Posts.Models.router)
app.include_router(app.Superuser.Models.router)

