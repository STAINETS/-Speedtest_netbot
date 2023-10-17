import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import speedtest

# Замените 'YOUR_BOT_TOKEN' на свой токен Telegram бота
BOT_TOKEN = '6447612984:AAFPUGRlnvT7xbVpR7cBXBQ8fiX-TEe3yGc'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Измерить скорость", callback_data='select_server')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Добро пожаловать в бот speedtest.net нажмите кнопку для измерения скорости интернета!", reply_markup=reply_markup)
def select_server(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text("Измеряю скорость интернета...")
    
    st = speedtest.Speedtest()
    st.get_best_server()
    
    try:
        download_speed = round(st.download() / 10**6, 2)
        upload_speed = round(st.upload() / 10**6, 2)
        query.edit_message_text(f"Скорость загрузки: {download_speed} Мбит/с\nСкорость выгрузки: {upload_speed} Мбит/с")
    except Exception as e:
        query.edit_message_text(f"Ошибка при измерении скорости: {e}")

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(select_server, pattern='^select_server$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
