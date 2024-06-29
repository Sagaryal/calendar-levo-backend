from fastapi import APIRouter, Depends, HTTPException, status
from pytz import utc
from sqlalchemy.orm import Session
from app import database
from . import crud, schemas, models
from app.users.models import User
from app.dependencies import get_current_user
from app.tasks import send_reminder_email

# from app.celery.tasks import send_notification

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    conflicting_event = (
        db.query(models.Event)
        .filter(
            models.Event.user_id == current_user.id,
            models.Event.start_time < event.end_time,
            models.Event.end_time > event.start_time,
        )
        .first()
    )

    if conflicting_event:
        conflicting_event_data = schemas.Event.model_validate(conflicting_event)
        conflicting_event_data.start_time = (
            conflicting_event_data.start_time.isoformat()
        )
        conflicting_event_data.end_time = conflicting_event_data.end_time.isoformat()

        raise HTTPException(
            status_code=400,
            detail={
                "error": "Conflict",
                "message": "Event conflicts with an existing event",
                "event": conflicting_event_data.model_dump(),
            },
        )

    db_event = crud.create_event(db, event, current_user.id)
    start_time = db_event.start_time
    start_time_utc = utc.localize(start_time)

    subject = f"Reminder: {db_event.title}"
    body = f"This is a reminder that the event '{db_event.title}' is scheduled to start at {db_event.start_time}."
    receipent_emails = [current_user.email]

    # send_reminder_email.delay(subject, body, receipent_emails, start_time)
    send_reminder_email.apply_async(
        (subject, body, receipent_emails), eta=start_time_utc
    )

    return db_event


@router.get("/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(database.get_db)):
    event = crud.get_event(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    event: schemas.EventUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    db_event = crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if db_event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this event",
        )

    return crud.update_event(db, db_event=db_event, event=event)


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    db_event = crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    if db_event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this event",
        )

    crud.delete_event(db, db_event)
    return {"message": f"Event {db_event.id} deleted successfully"}
