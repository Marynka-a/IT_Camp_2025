from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import models, schemas

# Користувачі

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Події

def get_event(db: Session, event_id: int) -> Optional[models.Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[models.Event]:
    return db.query(models.Event).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time
    )
    # Додаємо учасників, якщо є
    if event.participants:
        users = db.query(models.User).filter(models.User.id.in_(event.participants)).all()
        db_event.participants = users

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventCreate) -> Optional[models.Event]:
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    db_event.title = event_update.title
    db_event.description = event_update.description
    db_event.start_time = event_update.start_time
    db_event.end_time = event_update.end_time

    if event_update.participants:
        users = db.query(models.User).filter(models.User.id.in_(event_update.participants)).all()
        db_event.participants = users
    else:
        db_event.participants = []

    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True
