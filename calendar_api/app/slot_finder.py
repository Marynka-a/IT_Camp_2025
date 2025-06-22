# calendar_api/app/slot_finder.py

from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from .models import Event

def find_nearest_common_slot(
    all_events: List[Event],
    participants_ids: List[int],
    duration_minutes: int = 60,
    search_days: int = 7,
    start_hour: int = 9,
    end_hour: int = 18,
    now: Optional[datetime] = None
) -> List[Tuple[datetime, datetime]]:
    """
    Пошук найближчого вільного слота для всіх учасників.
    """
    if now is None:
        now = datetime.now()
    now = now.replace(minute=0, second=0, microsecond=0)

    delta = timedelta(minutes=duration_minutes)
    slots = []

    for day in range(search_days):
        current_day = now + timedelta(days=day)
        for hour in range(start_hour, end_hour):
            slot_start = current_day.replace(hour=hour)
            slot_end = slot_start + delta

            if all(is_slot_free(slot_start, slot_end, all_events, user_id) for user_id in participants_ids):
                slots.append((slot_start, slot_end))
                return slots  # Повертаємо перший знайдений слот

    return []

def is_slot_free(start: datetime, end: datetime, events: List, user_id: int) -> bool:
    """
    Перевірка, чи є слот вільним для конкретного користувача.
    """
    for event in events:
        if user_id not in event.participants:
            continue
        if start < event.end and end > event.start:
            return False
    return True
