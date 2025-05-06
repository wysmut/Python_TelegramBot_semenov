   import telegram
   from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
   from secrets import API_TOKEN

   def start(update, context):
       context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я ваш бот.")

   def echo(update, context):
       context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

   if __name__ == '__main__':
       updater = Updater(token=API_TOKEN, use_context=True)
       dispatcher = updater.dispatcher

       start_handler = CommandHandler('start', start)
       dispatcher.add_handler(start_handler)

       echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
       dispatcher.add_handler(echo_handler)

       updater.start_polling()
   
