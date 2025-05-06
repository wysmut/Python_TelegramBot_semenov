from sqlalchemy import Column, Integer, String, Date, DateTime
from bot.utils.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(500))
    date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer)
