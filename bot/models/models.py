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
    
class CalendarEvent(models.Model):
    # ... существующие поля ...
    
    @classmethod
    def create_from_telegram_event(cls, telegram_event, owner):
        """Создает событие Django из события Telegram бота"""
        return cls.objects.create(
            title=telegram_event.title,
            description=telegram_event.description,
            start_time=telegram_event.start_time,
            end_time=telegram_event.end_time,
            owner=owner
        )

    def to_telegram_event(self):
        """Конвертирует событие Django в формат для Telegram бота"""
        return {
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class UserStats(models.Model):
    # ... существующие поля ...
    
    def update_stats(self):
        """Обновляет статистику пользователя"""
        self.events_created = CalendarEvent.objects.filter(owner=self.user).count()
        self.events_participated = EventParticipation.objects.filter(user=self.user).count()
        self.save()
