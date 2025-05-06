from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.database import get_db
from bot.utils.db_operations import DBOperations
from bot.utils.calendar_utils import Calendar

def handle_calendar(update: Update, context: CallbackContext):
    db = next(get_db())
    user = DBOperations.get_or_create_user(
        db,
        update.effective_user.id,
        update.effective_user.username,
        update.effective_user.first_name,
        update.effective_user.last_name
    )
    
    calendar = Calendar()
    reply_markup = calendar.create_calendar()
    
    update.message.reply_text(
        "Пожалуйста, выберите дату:",
        reply_markup=reply_markup
    )

def handle_event_creation(update: Update, context: CallbackContext):
    db = next(get_db())
    user = DBOperations.get_or_create_user(db, update.effective_user.id)
    
    # Пример создания события
    new_event = DBOperations.create_event(
        db,
        user_id=user.id,
        title="Встреча",
        description="Обсуждение проекта",
        start_time=datetime(2023, 12, 15, 14, 0),
        end_time=datetime(2023, 12, 15, 15, 0)
    )
    
    update.message.reply_text(f"Событие '{new_event.title}' создано!")
