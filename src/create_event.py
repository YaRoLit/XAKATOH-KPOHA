from datetime import datetime, timedelta
from telebot import TeleBot, types
import sys
import re
import settings
import random
import temporaryStorage
import handler
import handle_event

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
    temp = tgbot.send_message(message.chat.id, f"Занятые временные интервалы в этот день:\n{busy_intervals_text}\nВведите время проведения события (например, 00:00-01:30):", reply_markup=markup)
    tgbot.register_next_step_handler(message, handle_event_time, tgbot, temp)

def handle_event_time(message, tgbot, temp):
    event_time = message.text
    tgbot.delete_message(chat_id=temp.chat.id, message_id=temp.message_id)
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if not re.match(r'^\d{2}:\d{2}-\d{2}:\d{2}$', event_time):
        temp = tgbot.send_message(message.chat.id, "Некорректный формат времени. Пожалуйста, введите время в формате 00:00-01:30")
        tgbot.register_next_step_handler(message, handle_event_time, tgbot, temp)
        return

    start_time, end_time = event_time.split('-')
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    duration = int((end_dt - start_dt).total_seconds() // 60)

    event_data[message.chat.id]['time'] = start_time
    event_data[message.chat.id]['duration'] = duration



    choose_tags(tgbot, message)

def choose_tags(tgbot, message):
    handle_event_tags(tgbot, message)

def handle_event_tags(tgbot, call, added='', removed=''):

    try:

        if 'tags' not in event_data[call.message.chat.id]:
            event_data[call.message.chat.id]['tags'] = []
            
        selected_tags = event_data[call.message.chat.id]['tags']

        if (added != ''):
            selected_tags.append(added)
        elif (removed != ''):
            selected_tags.remove(removed)
    except:
        if 'tags' not in event_data[call.chat.id]:
            event_data[call.chat.id]['tags'] = []
            
        selected_tags = event_data[call.chat.id]['tags']

        if (added != ''):
            selected_tags.append(added)
        elif (removed != ''):
            selected_tags.remove(removed)

    markup = types.InlineKeyboardMarkup(row_width=2)
    for tag in tags:
        if tag in selected_tags: #ЗАПРОС К БД
            markup.add(types.InlineKeyboardButton("✅ " + tag, callback_data=f"tag_to_event_rm {tag}"))
        else:
            markup.add(types.InlineKeyboardButton(tag, callback_data=f"tag_to_event_add {tag}"))

    markup.add(types.InlineKeyboardButton("Готово", callback_data=f"choose_title"))
    #except Exception as e:
        #print(e)
    try:
        
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Добавьте теги:", reply_markup=markup)
    except:
        tgbot.send_message(call.chat.id, f"Добавьте теги:", reply_markup=markup)


def choose_title(tgbot, call):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    tgbot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    temp = tgbot.send_message(chat_id=call.message.chat.id, text="Введите название события:", reply_markup=markup)
    tgbot.register_next_step_handler(call.message, handle_event_title, tgbot, temp)

def handle_event_title(message, tgbot, temp):
    event_title = message.text
    event_data[message.chat.id]['title'] = event_title
    choose_description(tgbot, message, temp)

def choose_description(tgbot, message, temp):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    tgbot.delete_message(chat_id=temp.chat.id, message_id=temp.message_id)
    temp = tgbot.send_message(chat_id=message.chat.id, text="Введите описание события:", reply_markup=markup)
    tgbot.register_next_step_handler(message, handle_event_description, tgbot, temp)

def handle_event_description(message, tgbot, temp):
    event_description = message.text
    tgbot.delete_message(chat_id=temp.chat.id, message_id=temp.message_id)
    event_data[message.chat.id]['description'] = event_description
    choose_speakers(tgbot, message)

def choose_speakers(tgbot, call):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    tgbot.delete_message(chat_id=call.chat.id, message_id=call.message_id)
    temp = tgbot.send_message(chat_id=call.chat.id, text="Какие спикеры присутствуют?", reply_markup=markup)
    tgbot.register_next_step_handler(call, handle_event_speakers, tgbot, temp)

def handle_event_speakers(message, tgbot, temp):
    speakers = message.text
    event_data[message.chat.id]['speakers'] = speakers
    finalize_event(tgbot, message, temp)

def finalize_event(tgbot, message, temp):
    event = event_data[message.chat.id]
    event_datetime = datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")

    creator= message.chat.id
    speakers= event['speakers']
    _datetime=event_datetime
    long=event['duration']
    event_type=event['type']
    city=event['city']
    place=event['place']
    tags=','.join(event['tags'])
    event_name=event['title']
    description=event['description']
    event_id= random.randint(1000, 9999)
    id = temporaryStorage.createEvent.create_task_in_Storage(
        creator= message.chat.id,
        speakers= event['speakers'],
        datetime=event_datetime,
        long=event['duration'],
        event_type=event['type'],
        city=event['city'],
        place=event['place'],
        tags=','.join(event['tags']),
        event_name=event['title'],
        description=event['description'],
        event_id=event_id
    )

    handle_event.adminNotify(tgbot, id, _datetime, long, event_type, city, place, tags, event_name, description, creator, speakers, event_id)



    summary = (f"Тип события: {event['type']}\n" +
               f"Дата: {event['date']}\n" +
               f"Город: {event['city']}\n" +
               f"Место: {event['place']}\n" +
               f"Время: {event['time']}\n" +
               f"Длительность: {long} минут"
               f"Теги: {', '.join(event['tags'])}\n" +
               f"Название: {event['title']}\n" +
               f"Описание: {event['description']}")

    tgbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    tgbot.delete_message(chat_id=temp.chat.id, message_id=temp.message_id)
    tgbot.send_message(message.chat.id, f"Событие отправлено на рассмотрение:\n{summary}")
