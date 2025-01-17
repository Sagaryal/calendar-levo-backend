from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.router import UsersRouter, EventsRouter
from app.config import settings
import uvicorn

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Levo Calendar Management",
    version="0.1.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UsersRouter, prefix="/api")
app.include_router(EventsRouter, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Levo Calendar Scheduling Application"}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
