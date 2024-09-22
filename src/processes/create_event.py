from datetime import datetime, timedelta
from telebot import TeleBot, types
import importlib.util
import sys
import importlib

# Укажите путь к вашему settings.py
settings_path = 'settings.py'

# Загрузите модуль settings
spec = importlib.util.spec_from_file_location("settings", settings_path)
settings = importlib.util.module_from_spec(spec)
sys.modules["settings"] = settings
spec.loader.exec_module(settings)

cities = settings.cities
event_types = settings.types
tags = settings.tags
event_data = {}
events = settings.events
users = settings.users


def update_settings():
    global events
    global users
    global cities
    global types
    global tags
    settings.cities = cities
    settings.types = event_types
    settings.events = events
    settings.users = users
    settings.tags = tags
    importlib.reload(settings)



def event_create_start(tgbot, call):
    event_data[call.message.chat.id] = {}
    choose_event_type(tgbot, call)

def choose_event_type(tgbot, call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for event_type in event_types:
        markup.add(types.InlineKeyboardButton(event_type, callback_data=f"event_type {event_type}"))
    tgbot.delete_message(call.message.chat.id, call.message.message_id)
    tgbot.send_message(call.message.chat.id, "Выберите тип события:", reply_markup=markup)

def handle_event_type(tgbot, call):
    event_type = call.data.split()[1]
    event_data[call.message.chat.id]['type'] = event_type
    choose_date(tgbot, call.message)

def choose_date(tgbot, message):
    markup = types.InlineKeyboardMarkup(row_width=7)
    start_date = datetime.now()
    start_date = start_date.replace(day=1)
    week_day = (start_date.weekday() - 2)
    days = []

    # Заполнение списка датами на 30 дней вперед
    for i in range(30):
        day = start_date + timedelta(days=i)
        days.append(day.strftime('%Y-%m-%d'))

    buttons = []
    for day in days:
        _day = day.split('-')[2]
        buttons.append(types.InlineKeyboardButton(_day, callback_data=f"event_date {day}"))

    buttons_empty = []
    for i in range(week_day):
        buttons_empty.append(types.InlineKeyboardButton("ㅤ", callback_data=f"empty"))

    days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    days_of_week_buttons = []
    for day in days_of_week:
        days_of_week_buttons.append(types.InlineKeyboardButton(day, callback_data=f"empty"))

    for i in range(0, len(days_of_week_buttons), 7):
        markup.add(*days_of_week_buttons[i:i+7])

    # Если в buttons_empty меньше 7 кнопок, добавляем из buttons
    while len(buttons_empty) < 7:
        buttons_empty.append(buttons.pop(0))

    for i in range(0, len(buttons_empty), 7):
        markup.add(*buttons_empty[i:i+7])

    # Добавляем кнопки в разметку по 7 в ряд
    for i in range(0, len(buttons), 7):
        markup.add(*buttons[i:i+7])

    tgbot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите дату:", reply_markup=markup)

def handle_event_date(tgbot, call):
    event_date = call.data.split()[1]
    event_data[call.message.chat.id]['date'] = event_date
    choose_city(tgbot, call.message)

def choose_city(tgbot, message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for city in cities.keys():
        markup.add(types.InlineKeyboardButton(city, callback_data=f"event_city {city}"))
    tgbot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите город:", reply_markup=markup)

def handle_event_city(tgbot, call):
    event_city = call.data.split()[1]
    event_data[call.message.chat.id]['city'] = event_city
    choose_place(tgbot, call.message, event_city)

def choose_place(tgbot, message, city):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for place in cities[city]:
        markup.add(types.InlineKeyboardButton(place, callback_data=f"event_place {place}"))
    tgbot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите место:", reply_markup=markup)

def handle_event_place(tgbot, call):
    event_place = call.data.split()[1]
    event_data[call.message.chat.id]['place'] = event_place
    choose_time(tgbot, call.message)

def choose_time(tgbot, message):
    event_date = event_data[message.chat.id]['date']
    event_city = event_data[message.chat.id]['city']
    event_place = event_data[message.chat.id]['place']
    date_start = datetime.strptime(event_date, "%Y-%m-%d")
    busy_times = events.check_datetime(date_start, 1440)  # Проверяем занятость на весь день

    busy_intervals = []
    for _, row in busy_times.iterrows():
        busy_intervals.append(f"{row['datetime'].strftime('%H:%M')} - {row['datetime'].strftime('%H:%M')}")

    busy_intervals_text = "\n".join(busy_intervals) if busy_intervals else "Нет занятых временных интервалов."

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    temp = tgbot.send_message(message.chat.id, f"Занятые временные интервалы в этот день:\n{busy_intervals_text}\nВведите время проведения события (например, 18:00):", reply_markup=markup)
    tgbot.register_next_step_handler(message, handle_event_time, tgbot, temp)

def handle_event_time(message, tgbot, temp):
    event_time = message.text
    event_data[message.chat.id]['time'] = event_time
    choose_tags(tgbot, message, temp)

def choose_tags(tgbot, message, temp):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for tag in tags:
        markup.add(types.InlineKeyboardButton(tag, callback_data=f"event_tag {tag}"))
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    tgbot.delete_message(chat_id=temp.chat.id, message_id=temp.message_id)
    tgbot.send_message(chat_id=message.chat.id, text="Выберите подходящие теги:", reply_markup=markup)

def handle_event_tags(tgbot, call):
    tag = call.data.split()[1]
    if 'tags' not in event_data[call.message.chat.id]:
        event_data[call.message.chat.id]['tags'] = []
    event_data[call.message.chat.id]['tags'].append(tag)
    choose_title(tgbot, call.message)

def choose_title(tgbot, message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    tgbot.send_message(chat_id=message.chat.id, text="Введите название события:", reply_markup=markup)
    tgbot.register_next_step_handler(message, handle_event_title, tgbot)

def handle_event_title(message, tgbot):
    event_title = message.text
    event_data[message.chat.id]['title'] = event_title
    choose_description(tgbot, message)

def choose_description(tgbot, message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    tgbot.send_message(chat_id=message.chat.id, text="Введите описание события:", reply_markup=markup)
    tgbot.register_next_step_handler(message, handle_event_description, tgbot)

def handle_event_description(message, tgbot):
    event_description = message.text
    event_data[message.chat.id]['description'] = event_description
    finalize_event(tgbot, message)

def finalize_event(tgbot, message):
    event = event_data[message.chat.id]
    event_datetime = datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
    new_event = {
        'datetime': event_datetime,
        'type': event['type'],
        'city': event['city'],
        'place': event['place'],
        'tags': ','.join(event['tags']),
        'title': event['title'],
        'description': event['description']
    }
    #scheduler.add_event(new_event)
    #scheduler.bd_save()
    summary = (f"Тип события: {event['type']}\n"
               f"Дата: {event['date']}\n"
               f"Город: {event['city']}\n"
               f"Место: {event['place']}\n"
               f"Время: {event['time']}\n"
               f"Теги: {', '.join(event['tags'])}\n"
               f"Название: {event['title']}\n"
               f"Описание: {event['description']}")
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    tgbot.send_message(message.chat.id, f"Событие создано:\n{summary}")
