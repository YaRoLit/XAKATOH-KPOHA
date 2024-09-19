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
import handler


# Инициализация бота
tgbot = tgbot.TeleBot(settings.TELEGRAM_TOKEN)
settings.tgbot = tgbot


# Словарь для хранения данных пользователей
users = settings.users

tags = {"Игры": 0, "Деньги": 0}


@tgbot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    if username not in users: #ЗАПРОС К БД
        users[username] = User(message.chat.id, username) #ЗАПРОС К БД (На добавление)

        tgbot.send_message(message.chat.id, f"Добро пожаловать, {username}!")
    tgbot.delete_message(message.chat.id, message.message_id)
    tag_select(message)


# _________________МЕНЮ_________________

def tag_select(call):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    for tag in tags.keys():
        if tag in users[call.from_user.username].tags: #ЗАПРОС К БД
            markup.add(types.InlineKeyboardButton("✅ " + tag, callback_data=f"tag_to_user_remove {tag}"))
        else:
            markup.add(types.InlineKeyboardButton(tag, callback_data=f"tag_to_user_add {tag}"))

    markup.add(types.InlineKeyboardButton("Готово", callback_data=f"to_main_menu"))
    #except Exception as e:
        #print(e)
    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Что вас интересует?", reply_markup=markup)
    except:
        main = tgbot.send_message(call.chat.id, f"Что вас интересует?", reply_markup=markup)

def main_menu(call):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    market = types.InlineKeyboardButton("🚀 Создать", callback_data="create_event")
    wallet = types.InlineKeyboardButton("📅 Календарь", callback_data="calendar")
    markup.add(market, wallet)
                                                                                                                                                # Нереализованный функционал Веб-приложения
                                                                                                                                                #web_app_info = types.WebAppInfo("https://localhost:5000")
                                                                                                                                                #button = types.KeyboardButton(text="Веб-приложение", web_app=web_app_info)
                                                                                                                                                #markup.add(button)
    #except Exception as e:
        #print(e)
    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Главное меню", reply_markup=markup)
    except:
        main = tgbot.send_message(call.message.chat.id, f"Главное меню", reply_markup=markup)


# ______________________________________


if __name__ == "__main__":

    tgbot.polling(none_stop=True)
