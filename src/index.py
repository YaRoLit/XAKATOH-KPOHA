import telebot as tgbot
from telebot import types
from telebot.apihelper import ApiTelegramException
import threading
import time
import settings
import json
import random
import string
from player import Player


# Инициализация бота
tgbot = tgbot.TeleBot(settings.TELEGRAM_TOKEN)


# Словарь для хранения данных пользователей
users = settings.users

tags = {"Игры": 0, "Деньги": 0}


@tgbot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    if username not in users:
        users[username] = Player(message.chat.id, username)

        tgbot.send_message(message.chat.id, f"Добро пожаловать, {username}!")
    tgbot.delete_message(message.chat.id, message.message_id)
    tag_select(message)


# _________________МЕНЮ_________________

def tag_select(call):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        for tag in tags.keys():
            if tag in users[call.from_user.username].tags:
                markup.add(types.InlineKeyboardButton("✅ " + tag, callback_data=f"tag_to_user_remove {tag}"))
            else:
                markup.add(types.InlineKeyboardButton(tag, callback_data=f"tag_to_user_add {tag}"))

        markup.add(types.InlineKeyboardButton("Готово", callback_data=f"to_main_menu"))
    except Exception as e:
        print(e)
    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Что вас интересует?", reply_markup=markup)
    except:
        main = tgbot.send_message(call.chat.id, f"Что вас интересует?", reply_markup=markup)

def main_menu(call):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        market = types.InlineKeyboardButton("🚀 Создать", callback_data="create_event")
        wallet = types.InlineKeyboardButton("📅 Календарь", callback_data="calendar")
        markup.add(market, wallet)
    except Exception as e:
        print(e)
    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Главное меню", reply_markup=markup)
    except:
        main = tgbot.send_message(call.chat.id, f"Главное меню", reply_markup=markup)


# ______________________________________

@tgbot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data.split(" ", 1)[0] == "tag_to_user_add":
            username = call.from_user.username
            users[username].tags.append(call.data.split(" ")[1])
            tag_select(call)
        
        elif call.data.split(" ", 1)[0] == "tag_to_user_remove":
            username = call.from_user.username
            users[username].tags.remove(call.data.split(" ")[1])
            tag_select(call)
        
        elif call.data.split(" ", 1)[0] == "to_main_menu":
            main_menu(call)

        else:
            tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)


    except Exception as e:
        tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)
        print(e)



if __name__ == "__main__":

    tgbot.polling(none_stop=True)
