import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DATABASE_URL: str = "postgresql://user:password@localhost/calendar"
    DATABASE_URL: str = "sqlite:///./calender_levo.db"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    HOLIDAY_API_KEY: str = os.getenv("HOLIDAY_API_KEY", "your_api_key_here")

    PORT: int = 8000


settings = Settings()
