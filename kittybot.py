import logging
import os
import sys

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)


def get_new_cat_image():
    URL = "https://api.thecatapi.com/v1/images/search"
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f"Ошибка при запросе к основному API: {error}")
        new_url = "https://api.thedogapi.com/v1/images/search"
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get("url")
    return random_cat


def get_new_dog_image():
    URL = "https://api.thedogapi.com/v1/images/search"
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f"Ошибка при запросе к основному API: {error}")
        new_url = "https://api.thedocatapi.com/v1/images/search"
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get("url")
    return random_dog


def new_cat(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup(
        [["Покажи котика!"], ["Покажи собачку!"]], resize_keyboard=True
    )
    context.bot.send_photo(
        chat.id,
        get_new_cat_image(),
        reply_markup=buttons,
    )


def new_dog(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup(
        [["Покажи котика!"], ["Покажи собачку!"]], resize_keyboard=True
    )
    context.bot.send_photo(
        chat.id,
        get_new_dog_image(),
        reply_markup=buttons,
    )


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup(
        [["Покажи котика!"], ["Покажи собачку!"]], resize_keyboard=True
    )

    context.bot.send_message(
        chat_id=chat.id,
        text=f"Привет, {name}. Кого хочешь, чтобы я тебе показал?",
        reply_markup=buttons,
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text("Покажи котика!"), new_cat)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text("Покажи собачку!"), new_dog)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
