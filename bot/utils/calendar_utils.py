from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from datetime import datetime

calendar_callback = CallbackData('calendar', 'act', 'year', 'month', 'day')

def create_calendar(year=None, month=None):
    now = datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    
    keyboard = InlineKeyboardMarkup(row_width=7)
    
    keyboard.row(
        InlineKeyboardButton("<<", callback_data=calendar_callback.new("PREV-YEAR", year, month, 0)),
        InlineKeyboardButton(f"{datetime(year, month, 1).strftime('%B %Y')}", callback_data="IGNORE"),
        InlineKeyboardButton(">>", callback_data=calendar_callback.new("NEXT-YEAR", year, month, 0))
    )
    
    keyboard.row(*[
        InlineKeyboardButton(day, callback_data="IGNORE")
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    ])
    
    return keyboard
