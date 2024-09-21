import telebot as tgbot
from telebot import types
from telebot.apihelper import ApiTelegramException
import threading
import time
from nlp_requests import nlp_request
from response import render_eventlist
import settings
import json
import random
import string
from transcribator import Transcribator
from user import User
from processes import *
from handler import handle_msg
from menu import *
from pydub import AudioSegment
import torch

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

@tgbot.message_handler(content_types=['text'])
def handle_text(message):
    nlp_request(tgbot, message, message.text)

@tgbot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = tgbot.get_file(message.voice.file_id)
    file = tgbot.download_file(file_info.file_path)
    
    with open("cache/voice.ogg", 'wb') as f:
        f.write(file)
    
    # Конвертируем OGG в WAV
    audio = AudioSegment.from_ogg("cache/voice.ogg")
    audio.export("cache/voice.wav", format="wav")
    
    tr = Transcribator()
    text = tr.transcribe("cache/voice.wav")
    print("transcribed: " + text)
    
    df = nlp_request(tgbot, message, text)
    tgbot.send_message(chat_id=message.chat.id, text=render_eventlist(df))
    

if __name__ == "__main__":

    tgbot.polling(none_stop=True)