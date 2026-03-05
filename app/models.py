from pydantic import BaseModel, Field
from typing import Literal

Role = Literal["viewer", "admin"]

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    role: Role

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    role: Role = "viewer"   # default viewer

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    username: str
    role: Role