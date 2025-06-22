from fastapi import FastAPI
from .database import Base, engine
from .routes import events, users, participants
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="static", html=True), name="static")

app = FastAPI()

# Створюємо таблиці
Base.metadata.create_all(bind=engine)

# Підключаємо маршрути
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(participants.router, prefix="/participants", tags=["Participants"])
