from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.utils.calendar_utils import create_calendar

async def calendar_handler(message: types.Message):
    await message.answer("Выберите дату:", reply_markup=create_calendar())

async def process_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    pass

def register_handlers_calendar(dp: Dispatcher):
    dp.register_message_handler(calendar_handler, commands="calendar")
    dp.register_callback_query_handler(process_calendar, create_calendar().filter())
