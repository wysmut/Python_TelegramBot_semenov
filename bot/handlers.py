from telegram import Update
from telegram.ext import CallbackContext
from database import create_order

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Добро пожаловать! Используйте /order для оформления нового заказа.')

def order(update: Update, context: CallbackContext):
    update.message.reply_text('Пожалуйста, отправьте детали вашего заказа как текстовое сообщение.')
    context.user_data['ordering'] = True  # Флаг для состояния заказов

def message_handler(update: Update, context: CallbackContext):
    if context.user_data.get('ordering'):
        order_text = update.message.text
        order_id = create_order(order_text)
        
        if order_id:
            update.message.reply_text(f'Ваш заказ принят с ID: {order_id}. Спасибо за ваш заказ!')
        else:
            update.message.reply_text('Ошибка! Не удалось обработать ваш заказ.')

        context.user_data['ordering'] = False
    else:
        update.message.reply_text('Пожалуйста, используйте /order для начала оформления заказа.')
