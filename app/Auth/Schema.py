from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterNewUser(BaseModel):
    fullname: str
    username: str
    email: str = Field(regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")
    password: str = Field(regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")
    token: UUID = Field(default_factory=uuid4)
