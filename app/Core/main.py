from fastapi.staticfiles import StaticFiles
from . import database
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import models
from. import dependencies
import os



from ..Admin import AdminModels
from ..Auth import AuthModels
from ..Home import HomeModels
from ..Posts import PostsModels
from ..Superuser import SuperuserModels

app = FastAPI(dependencies=[Depends(dependencies.get_db)])
script_dir = os.path.dirname(__file__)[0:-5]
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
database.Base.metadata.create_all(bind=database.engine)

app.include_router(AdminModels.router)
app.include_router(AuthModels.router)
app.include_router(HomeModels.router)
app.include_router(PostsModels.router)
app.include_router(SuperuserModels.router)
