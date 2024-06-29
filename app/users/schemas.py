from pydantic import BaseModel, EmailStr
from app.events.schemas import Event


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    events: list[Event] = []

    class Config:
        from_attributes = True
