from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    title: str | None
    start_time: datetime | None
    end_time: datetime | None
    description: Optional[str] = None
    # participants: str
    # user_id: int


class EventCreate(EventBase):
    user_id: int


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
