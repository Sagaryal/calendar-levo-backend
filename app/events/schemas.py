from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    title: str | None
    start_time: datetime | None
    end_time: datetime | None
    description: Optional[str] = None
    # participants: str


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    description: Optional[str] = None


class Event(EventBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
