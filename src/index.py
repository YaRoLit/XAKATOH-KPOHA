import telebot as tgbot
from telebot import types
from telebot.apihelper import ApiTelegramException
import threading
import time
from nlp_requests import nlp_request
from response import render_eventlist, valueError_message
import settings
import importlib
import schedule
from transcribator import Transcribator
from users import Users
from create_event import *
from handler import handle_msg
from menu import *
from pydub import AudioSegment
from users import Users
from create_event import *
from handler import handle_msg
from menu import *
from scheduler import Scheduler
import tasks_planner

# Инициализация бота
tgbot = tgbot.TeleBot(settings.TELEGRAM_TOKEN)

# Словарь для хранения данных пользователей
users = settings.users
events = settings.events
cities = settings.cities
_types = settings.types

tags = settings.tags

def update_settings():
    global events
    global users
    global cities
    global types
    global tags
    settings.cities = cities
    settings.types = _types
    settings.events = events
    settings.users = users
    settings.tags = tags
    importlib.reload(settings)

update_settings()

@tgbot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.username
    if f'{user_id}' not in users.show_users().user_id.to_list():
        users.add_user(user_id=user_id, tags='')
        users.add_tag(user_id, "Игры")  # ЗАПРОС К БД
        users.bd_save()
        print(users.show_users())   

        tgbot.send_message(message.chat.id, f"Добро пожаловать, {username}!")
        tag_select(tgbot, message, user_id)
    else:
        print(users.show_users())   
        main_menu(tgbot, message)
    tgbot.delete_message(message.chat.id, message.message_id)

@tgbot.message_handler(commands=['id'])
def id(message):
    #settings.tap = 0
    tgbot.reply_to(message, f"{message.from_user.id}")


@tgbot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    handle_msg(tgbot, call)

#@tgbot.message_handler(content_types=['text'])
#def handle_text(message):
#    nlp_request(tgbot, message, message.text)


@tgbot.message_handler(content_types=['voice'])
def handle_voice(message):
    handle_event.notify_all(tgbot, "speakers", datetime(year=2024, month=9, day=22, hour=12, minute=30, second=00, microsecond=00), 
               60, "общий сбор", "Новосибирск", "Игровая", "#sex#drugs", "Название", "Описание.", 123123)
    # file_info = tgbot.get_file(message.voice.file_id)
    # file = tgbot.download_file(file_info.file_path)
    
    # with open("cache/voice.ogg", 'wb') as f:
    #     f.write(file)
    
    # # Конвертируем OGG в WAV
    # audio = AudioSegment.from_ogg("cache/voice.ogg")
    # audio.export("cache/voice.wav", format="wav")
    
    # tr = Transcribator()
    # text = tr.transcribe("cache/voice.wav")
    # print("transcribed: " + text)

    # nlp_request(tgbot, message, text)
    
def markup_Yes_No():
    markup = types.InlineKeyboardMarkup()
    buttonYes = types.InlineKeyboardButton('✅', callback_data='Yes')
    buttonNo = types.InlineKeyboardButton('❌', callback_data='No')
    markup.row(buttonYes, buttonNo)
    return markup

def not_add_event(message):
    markup = markup_Yes_No()
    tgbot.send_message(message.chat.id, "На это время уже запланированно мероприятие, отменить предыдущее и запланировать новое?", reply_markup=markup)

def cmd():
    while True:
        command = input("CMD: ")
        try:
            if (command.split(' ')[0] == 'city_add'):
                city = command.split(' ')[1]
                if city not in cities.keys():
                    cities[command.split(' ')[1]] = []
                else:
                    print("This city is already exists.")

            elif (command.split(' ')[0] == 'city_rm'):
                if (command.split(' ')[1] in cities):
                    cities.pop(command.split(' ')[1], None)
                else:
                    print('Undefined city.')

            elif (command.split(' ')[0] == 'places_add'):
                city = command.split(' ')[1]
                place = command.split(' ')[2]
                if (city in cities.keys()):
                    if place not in cities.values():
                        cities[city].append(place)
                    else:
                        print("This place is already exists.")
                else:
                    print('Undefined city.')

            elif (command.split(' ')[0] == 'places_rm'):
                if (command.split(' ')[1] in places.keys() and command.split(' ')[2] in places.values()):
                    city = command.split(' ')[1]
                    place = command.split(' ')[2]
                    cities[city].remove(place)
                else:
                    print("Incorrect input.")

            elif (command.split(' ')[0] == 'types_add'):
                tpe = command.split(' ')[1]                     # tpe = type
                if (tpe not in types):
                    types.append(tpe)
                else:
                    print("This type is already exists.")

            elif (command.split(' ')[0] == 'types_rm'):
                tpe = command.split(' ')[1]                     # tpe = type
                if (tpe in types):
                    types.remove(tpe)
                else:
                    print("Unknown type.")

            elif (command.split(' ')[0] == 'tags_add'):
                tag = command.split(' ')[1]
                if (tag not in tags):
                    tags.append(tag)
                else:
                    print("This Tag already exists.")

            elif (command.split(' ')[0] == 'tags_rm'):
                tag = command.split(' ')[1]
                if (tag in tags):
                    tags.remove(tag)
                else:
                    print("Unknown tag.")
            else:
                print("Wrong command.")
            update_settings()
        except Exception as e:
            print(e)
            print("Wrong command.")

if __name__ == "__main__":
    threading.Thread(target=cmd, args=()).start()
    threading.Thread(target=tasks_planner.run_scheduler).start()
    tgbot.polling(none_stop=True)
