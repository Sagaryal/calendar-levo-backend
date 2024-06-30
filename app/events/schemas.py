from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional
from pytz import utc


class EventBase(BaseModel):
    title: str | None
    start_time: datetime | None
    end_time: datetime | None
    description: Optional[str] = None


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

    @model_validator(mode="after")
    def convert_to_utc(cls, values):
        values.start_time = utc.localize(values.start_time)
        values.end_time = utc.localize(values.end_time)
        return values

    class Config:
        from_attributes = True
