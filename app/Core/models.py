from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    username = Column(String,unique=True)
    phone = Column(String,unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment",back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    create_date = (String)
    view_count = (Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    confirmed = Column(Boolean,default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User",back_populates="comments")


class message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    created_by = Column(String)
    date_created = Column(String)
    email = Column(String)
    description = Column(String)
    read = Column(Boolean,default=False)