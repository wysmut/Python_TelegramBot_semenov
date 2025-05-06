from datetime import datetime
from sqlalchemy.orm import Session
from bot.models.models import User, Event, SharedEvent

class DBOperations:
    @staticmethod
    def get_or_create_user(db: Session, telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def create_event(db: Session, user_id: int, title: str, description: str, 
                    start_time: datetime, end_time: datetime):
        event = Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            user_id=user_id
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_user_events(db: Session, user_id: int):
        return db.query(Event).filter(Event.user_id == user_id).all()

    @staticmethod
    def share_event(db: Session, event_id: int, recipient_id: int, can_edit: bool = False):
        shared_event = SharedEvent(
            event_id=event_id,
            user_id=recipient_id,
            can_edit=can_edit
        )
        db.add(shared_event)
        db.commit()
        return shared_event

    @staticmethod
    def get_shared_events(db: Session, user_id: int):
        return db.query(Event).join(SharedEvent).filter(SharedEvent.user_id == user_id).all()
