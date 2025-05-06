from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from datetime import datetime

calendar_callback = CallbackData('calendar', 'act', 'year', 'month', 'day')

def create_calendar(year=None, month=None):
    now = datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("<<", callback_data=calendar_callback.new("PREV-YEAR", year, month, 0)))
    keyboard.row(*[InlineKeyboardButton(month, callback_data=calendar_callback.new("SET-MONTH", year, month, i+1)) for i, month in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])])
    keyboard.row(*[InlineKeyboardButton(month, callback_data=calendar_callback.new("SET-MONTH", year, month, i+7)) for i, month in enumerate(["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])])
    return keyboard
