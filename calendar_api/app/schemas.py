from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    participants: List[int] = []

class Event(EventBase):
    id: int
    participants: List[User] = []

    class Config:
        orm_mode = True
