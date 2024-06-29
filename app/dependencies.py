from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app import database
from app.users import crud


def get_current_user(db: Session = Depends(database.get_db), user_id: str = Header()):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

    return user
