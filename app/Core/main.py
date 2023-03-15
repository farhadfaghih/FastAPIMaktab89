from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import models
import dependencies
from database import engine

from ..Admin import AdminModels
from ..Auth import AuthModels
from ..Home import HomeModels
from ..Posts import PostsModels
from ..Superuser import SuperuserModels


models.Base.metadata.create_all(bind=engine)
app = FastAPI(dependencies=[Depends(dependencies.get_db)])

app.include_router(AdminModels.router)
app.include_router(AuthModels.router)
app.include_router(HomeModels.router)
app.include_router(PostsModels.router)
app.include_router(SuperuserModels.router)
