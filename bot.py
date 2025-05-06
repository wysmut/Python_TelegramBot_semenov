import psycopg2
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.base import Base
from app.core.users.models import User
from app.core.orders.models import Order, Product, OrderedProduct

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/calendar_bot')
Session = sessionmaker(bind=engine)

class Calendar:
    def __init__(self):
        self.session = Session()

    def create_event(self, user_id, event_name, event_date, event_time):
        with self.session() as session:
            session.execute(
                "INSERT INTO events (user_id, name, date, time) VALUES (:user_id, :name, :date, :time)",
                {'user_id': user_id, 'name': event_name, 'date': event_date, 'time': event_time}
            )
            session.commit()

    def read_event(self, user_id, event_name):
        with self.session() as session:
            result = session.execute(
                "SELECT name, date, time FROM events WHERE user_id = :user_id AND name = :name",
                {'user_id': user_id, 'name': event_name}
            )
            return result.fetchone()

    def edit_event(self, user_id, event_name, new_date=None, new_time=None):
        with self.session() as session:
            if new_date:
                session.execute(
                    "UPDATE events SET date = :date WHERE user_id = :user_id AND name = :name",
                    {'date': new_date, 'user_id': user_id, 'name': event_name}
                )
            if new_time:
                session.execute(
                    "UPDATE events SET time = :time WHERE user_id = :user_id AND name = :name",
                    {'time': new_time, 'user_id': user_id, 'name': event_name}
                )
            session.commit()

    def delete_event(self, user_id, event_name):
        with self.session() as session:
            session.execute(
                "DELETE FROM events WHERE user_id = :user_id AND name = :name",
                {'user_id': user_id, 'name': event_name}
            )
            session.commit()

    def display_events(self, user_id):
        with self.session() as session:
            result = session.execute(
                "SELECT name, date, time FROM events WHERE user_id = :user_id",
                {'user_id': user_id}
            )
            return result.fetchall()

def main():
    from secrets import API_TOKEN
    Base.metadata.create_all(engine)
    
    calendar = Calendar()
    updater = Updater(API_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("create_event", create_event))
    dp.add_handler(CommandHandler("read_event", read_event))
    dp.add_handler(CommandHandler("edit_event", edit_event))
    dp.add_handler(CommandHandler("delete_event", delete_event))
    dp.add_handler(CommandHandler("display_events", display_events))
    dp.add_handler(CommandHandler("register", register))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
