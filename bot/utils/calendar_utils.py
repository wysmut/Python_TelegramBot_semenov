from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Calendar:
    def __init__(self):
        self.weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    
    def create_calendar(self, year=None, month=None):
        if year is None or month is None:
            now = datetime.now()
            year, month = now.year, now.month
        
        keyboard = []
  
        # Month and year header
        month_name = datetime(year, month, 1).strftime('%B %Y')
        keyboard.append([InlineKeyboardButton(month_name, callback_data="ignore")])
        
        # Weekdays header
        keyboard.append([
            InlineKeyboardButton(day, callback_data="ignore") for day in self.weekdays
        ])
        
        # Days
        first_day = datetime(year, month, 1)
        days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day
        offset = first_day.weekday()
        
        row = []
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            row.append(InlineKeyboardButton(str(day), callback_data=f"calendar_day_{date.strftime('%Y-%m-%d')}"))
            
            if (day + offset) % 7 == 0:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        # Navigation
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        
        navigation = [
            InlineKeyboardButton("<", callback_data=f"calendar_month_{prev_year}-{prev_month}"),
            InlineKeyboardButton("Today", callback_data="calendar_today"),
            InlineKeyboardButton(">", callback_data=f"calendar_month_{next_year}-{next_month}")
        ]
        keyboard.append(navigation)
        
        return InlineKeyboardMarkup(keyboard)
