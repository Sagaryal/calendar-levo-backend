from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from . import crud, schemas, models

# from app.celery.tasks import send_notification

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    conflicting_event = (
        db.query(models.Event)
        .filter(
            models.Event.user_id == event.user_id,
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

    return crud.create_event(db, event)
    # Schedule notification
    # send_notification.apply_async((db_event.title, db_event.start_time))


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
    event_id: int, event: schemas.EventUpdate, db: Session = Depends(database.get_db)
):
    db_event = crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.update_event(db, db_event=db_event, event=event)


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(database.get_db)):
    db_event = crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    crud.delete_event(db_event)
    return {"message": f"Event {db_event.id} deleted successfully"}
