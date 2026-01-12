from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)
