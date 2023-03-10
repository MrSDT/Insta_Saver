import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, filters, CallbackContext
import instaloader
from telegram.constants import ParseMode
from queue import Queue
from telegram.ext import PicklePersistence

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_BOT_TOKEN = '5948179345:AAEcHxNG-V2vvn5RxshNaXXywL4Gw3yArBk'
def start(update: Update, context):
    update.message.reply_text('Welcome to the Instagram post downloader bot! Please send me the link to the Instagram post you want to download.')

def download_post(update: Update, context):
    url = update.message.text
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    context.bot.send_photo(chat_id=update.message.chat_id, photo=post.url, caption=post.caption)

def help(update: Update, context):
    update.message.reply_text('Send me the link to the Instagram post you want to download.')

def error(update: Update, context):
    logging.error(f'Update {update} caused error {context.error}')

def main():
    persistence = PicklePersistence(filename='my_bot_data')
    updater = Updater(token=TELEGRAM_BOT_TOKEN, persistence=persistence)
    dispatcher = updater.dispatcher

    # Registering all handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # other handlers

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
