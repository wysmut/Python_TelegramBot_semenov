import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.handlers import common, calendar, admin
from bot.secrets import TELEGRAM_TOKEN
from bot.utils.database import engine, Base

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)

Base.metadata.create_all(bind=engine)

common.register_handlers_common(dp)
calendar.register_handlers_calendar(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
