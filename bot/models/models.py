from sqlalchemy import Column, Integer, String, Date
from bot.utils.database import Base

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    user_id = Column(Integer)
