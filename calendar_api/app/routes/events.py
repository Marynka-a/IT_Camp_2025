from fastapi import Query, APIRouter, Depends
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session

from app.slot_finder import find_nearest_common_slot
from app import models
from app.database import get_db  

router = APIRouter()  

@router.get("/free-slots")
async def free_slots(
    participants: List[int] = Query(..., description="ID користувачів"),
    duration_minutes: int = Query(60, description="Тривалість слоту в хвилинах"),
    search_days: int = Query(1, description="Кількість днів для пошуку вперед"),
    db: Session = Depends(get_db)
):
    now = datetime.now()
    end_search = now + timedelta(days=search_days)

    events = db.query(models.Event).filter(models.Event.end_time >= now).all()
    
    slots = find_nearest_common_slot(events, participants, duration_minutes, search_days)
    return {"free_slots": [{"start": s[0], "end": s[1]} for s in slots]}
