from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import start, order, message_handler
from secret import TELEGRAM_API_KEY

def main():
    updater = Updater(TELEGRAM_API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("order", order))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
