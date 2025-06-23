from typing import Optional

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RoomBase(BaseModel):
    id: int
    owner_id: int
    player2_id: Optional[int]
    is_started: bool

    class Config:
        orm_mode = True