from pydantic import BaseModel
from app.events.schemas import Event


class UserBase(BaseModel):
    username: str
    email: str
    timezone: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    events: list[Event] = []

    class Config:
        from_attributes = True
