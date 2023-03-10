import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import instaloader
import os
from config import telegram_bot_token

def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello, I'm a bot that can download Instagram posts. Just send me the link to the post and I will send you the downloaded media."
    )


def download_post(update, context):
    post_url = update.message.text
    L = instaloader.Instaloader()

    # Login to Instagram (optional)
    # L.interactive_login("<username>")

    # Get post by url
    post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])

    # Download the media
    L.download_post(post, target=os.getcwd())

    # Send the media to the user
    for filename in os.listdir():
        if filename.startswith(post.shortcode):
            context.bot.send_document(chat_id=update.message.chat_id, document=open(filename, 'rb'))
            os.remove(filename)


updater = Updater(token=telegram_bot_token, use_context=True)

start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)

text_handler = MessageHandler(Filters.text & (~Filters.command), download_post)
updater.dispatcher.add_handler(text_handler)

updater.start_polling()
updater.idle()

