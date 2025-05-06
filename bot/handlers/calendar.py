from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.utils.calendar_utils import create_calendar
from bot.utils.database import get_db
from bot.models.models import Event
from datetime import date

async def calendar_handler(message: types.Message):
    await message.answer("Выберите дату:", reply_markup=create_calendar())

async def process_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    db = next(get_db())
    selected_date = date(
        int(callback_data['year']),
        int(callback_data['month']),
        int(callback_data['day'])
    )
    
    new_event = Event(
        title="Новое событие",
        date=selected_date,
        user_id=callback_query.from_user.id
    )
    
    db.add(new_event)
    db.commit()
    await callback_query.message.answer(f"Событие создано на {selected_date}")

def register_handlers_calendar(dp: Dispatcher):
    dp.register_message_handler(calendar_handler, commands="calendar")
    dp.register_callback_query_handler(process_calendar, create_calendar().filter())
