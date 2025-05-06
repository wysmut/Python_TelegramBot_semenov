from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command

async def admin_panel(message: types.Message):
    await message.answer("Админ панель")

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, Command("admin"), is_admin=True)
