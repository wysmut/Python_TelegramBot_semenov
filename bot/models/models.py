from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False)
    
    events = relationship("Event", back_populates="user")
    shared_events = relationship("SharedEvent", back_populates="user")

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="events")
    shared_with = relationship("SharedEvent", back_populates="event")

class SharedEvent(Base):
    __tablename__ = 'shared_events'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    can_edit = Column(Boolean, default=False)
    
    event = relationship("Event", back_populates="shared_with")
    user = relationship("User", back_populates="shared_events")
