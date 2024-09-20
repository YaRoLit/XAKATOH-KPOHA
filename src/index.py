import telebot as tgbot
from telebot import types
from telebot.apihelper import ApiTelegramException
import threading
import time
import settings
import json
import random
import string
from user import User
from processes import *
from handler import handle_msg
from menu import *


# Инициализация бота
tgbot = tgbot.TeleBot(settings.TELEGRAM_TOKEN)


# Словарь для хранения данных пользователей
users = settings.users

tags = settings.tags


@tgbot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    if username not in users: #ЗАПРОС К БД
        users[username] = User(message.chat.id, username) #ЗАПРОС К БД (На добавление)

        tgbot.send_message(message.chat.id, f"Добро пожаловать, {username}!")
    tgbot.delete_message(message.chat.id, message.message_id)
    tag_select(tgbot, message)


@tgbot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    handle_msg(tgbot, call)

if __name__ == "__main__":

    tgbot.polling(none_stop=True)
