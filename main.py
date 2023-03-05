from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
نحوه کار با دیتابیس


def get_users(db: Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Depends(Session), user: schemas.UserCreate): # از مدل پایدنتیک استفاده کن ورودی رو بگیر بعد باهاش یه اینستنس از کلاس دیتابیس بساز
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""