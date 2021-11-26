from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

# USER
class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# TOKEN
class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# POST
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse
    
    class Config:
        orm_mode = True

class PostWithVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

# VOTE
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
