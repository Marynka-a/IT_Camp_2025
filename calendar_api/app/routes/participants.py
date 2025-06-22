from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import database, models, schemas

router = APIRouter()
get_db = database.get_db

@router.get("/events/{event_id}/participants", response_model=List[schemas.User])
def get_event_participants(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.participants

@router.post("/events/{event_id}/participants", response_model=List[schemas.User])
def add_participants(event_id: int, user_ids: List[int], db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    # Додаємо нових учасників без дублювань
    current_ids = {u.id for u in event.participants}
    for user in users:
        if user.id not in current_ids:
            event.participants.append(user)
    db.commit()
    db.refresh(event)
    return event.participants

@router.delete("/events/{event_id}/participants/{user_id}")
def remove_participant(event_id: int, user_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or user not in event.participants:
        raise HTTPException(status_code=404, detail="Participant not found in event")
    event.participants.remove(user)
    db.commit()
    return {"detail": "Participant removed from event"}
