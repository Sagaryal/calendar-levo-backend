import datetime
from app.mail import send_email

from celery import Celery
from app.config import settings

import asyncio

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery_app.task
def send_reminder_email(subject: str, body: str, receipent_emails: list[str]):
    print("reminder, eumaisl", subject, body, receipent_emails)
    asyncio.run(send_email(subject, body, receipent_emails))


# celery_app.conf.update(task_track_started=True)
