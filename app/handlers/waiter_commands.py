from app.core.orders.services import OrderService
from telegram import Update
from telegram.ext import ContextTypes


async def waiter_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.effective_user:
        await context.application.user_service.register_visitor(update.effective_user.id)  # type: ignore[attr-defined]
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать на работу!")


async def waiter_finish_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    order_service: OrderService = context.application.order_service

    query = update.callback_query
    await query.answer()

    callback_data = query.data
    order_id = int(callback_data[1])
    await order_service.mark_order_done(order_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Заказ был переведён в завершённые"
    )
