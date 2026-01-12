from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime
from app.db.database import Base

class ChatLog(Base):
    __tablename__ = "abc"
    # __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
