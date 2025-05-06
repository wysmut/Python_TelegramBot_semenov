import psycopg2
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

class Calendar:
    def __init__(self, conn):
        self.conn = conn

    def create_event(self, user_id, event_name, event_date, event_time):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO events (user_id, name, date, time) VALUES (%s, %s, %s, %s)",
            (user_id, event_name, event_date, event_time)
        )
        self.conn.commit()

    def read_event(self, user_id, event_name):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name, date, time FROM events WHERE user_id = %s AND name = %s",
            (user_id, event_name)
        return cursor.fetchone()

    def edit_event(self, user_id, event_name, new_date=None, new_time=None):
        cursor = self.conn.cursor()
        if new_date:
            cursor.execute(
                "UPDATE events SET date = %s WHERE user_id = %s AND name = %s",
                (new_date, user_id, event_name))
        if new_time:
            cursor.execute(
                "UPDATE events SET time = %s WHERE user_id = %s AND name = %s",
                (new_time, user_id, event_name)
            )
        self.conn.commit()

    def delete_event(self, user_id, event_name):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM events WHERE user_id = %s AND name = %s",
            (user_id, event_name)
        )
        self.conn.commit()

    def display_events(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name, date, time FROM events WHERE user_id = %s",
            (user_id,)
        )
        return cursor.fetchall()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот-календарь. Используй /help для списка команд.')

def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        '/create_event <название> <дата> <время> - создать событие\n'
        '/read_event <название> - просмотреть событие\n'
        '/edit_event <название> [новая_дата] [новое_время] - изменить событие\n'
        '/delete_event <название> - удалить событие\n'
        '/display_events - показать все события\n'
        '/register - зарегистрироваться'
    )

def create_event(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        event_name = context.args[0]
        event_date = context.args[1]
        event_time = context.args[2]
        calendar.create_event(user_id, event_name, event_date, event_time)
        update.message.reply_text('Событие создано!')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /create_event <название> <дата> <время>')

def read_event(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        event_name = context.args[0]
        event = calendar.read_event(user_id, event_name)
        if event:
            update.message.reply_text(f'Событие: {event[0]}, Дата: {event[1]}, Время: {event[2]}')
        else:
            update.message.reply_text('Событие не найдено')
    except IndexError:
        update.message.reply_text('Использование: /read_event <название>')

def edit_event(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        event_name = context.args[0]
        new_date = context.args[1] if len(context.args) > 1 else None
        new_time = context.args[2] if len(context.args) > 2 else None
        calendar.edit_event(user_id, event_name, new_date, new_time)
        update.message.reply_text('Событие изменено!')
    except IndexError:
        update.message.reply_text('Использование: /edit_event <название> [новая_дата] [новое_время]')

def delete_event(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        event_name = context.args[0]
        calendar.delete_event(user_id, event_name)
        update.message.reply_text('Событие удалено!')
    except IndexError:
        update.message.reply_text('Использование: /delete_event <название>')

def display_events(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    events = calendar.display_events(user_id)
    if events:
        response = 'Ваши события:\n'
        for event in events:
            response += f'{event[0]} - {event[1]} {event[2]}\n'
        update.message.reply_text(response)
    else:
        update.message.reply_text('У вас нет событий')

def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
    conn.commit()
    update.message.reply_text('Вы зарегистрированы!')

def main():
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
    from secrets import API_TOKEN, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id bigint PRIMARY KEY
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id serial PRIMARY KEY,
        user_id bigint REFERENCES users(user_id),
        name text NOT NULL,
        date date NOT NULL,
        time time NOT NULL
    );
    """)
    conn.commit()
    calendar = Calendar(conn)
    main()
