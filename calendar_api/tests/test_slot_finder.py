# tests/test_slot_finder.py

from datetime import datetime, timedelta
from app.slot_finder import find_nearest_common_slot

# Фікстура для створення події
class MockEvent:
    def __init__(self, start, end, participants):
        self.start = start
        self.end = end
        self.participants = participants

def mock_event(start, end, participants):
    return MockEvent(start, end, participants)

def test_no_events_found():
    now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    events = []
    participants = [1, 2]
    slots = find_nearest_common_slot(events, participants, duration_minutes=60, search_days=1, now=now)
    assert slots, "Якщо немає подій, слоти повинні бути знайдені"

def test_no_slot_found():
    now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    # Створюємо події, які займають увесь день у учасників
    events = [
        mock_event(now.replace(hour=h), now.replace(hour=h+1), [1, 2])
        for h in range(9, 18)
    ]
    participants = [1, 2]

    slots = find_nearest_common_slot(events, participants, duration_minutes=60, search_days=1, now=now)
    print("DEBUG: знайдені слоти", slots)
    assert slots == [], "Слоти не повинні бути знайдені, якщо всі години зайняті"

def test_slot_found():
    now = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    events = [
        mock_event(now + timedelta(hours=9), now + timedelta(hours=10), [1]),
        mock_event(now + timedelta(hours=11), now + timedelta(hours=12), [2]),
    ]
    participants = [1, 2]

    slots = find_nearest_common_slot(events, participants, duration_minutes=60, search_days=1, now=now)
    assert any(slot[0] >= now for slot in slots), "Потрібен вільний слот після зайнятих годин"
