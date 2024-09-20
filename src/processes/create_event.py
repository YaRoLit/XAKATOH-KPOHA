# Процесс для создания события
from datetime import datetime, timedelta
from telebot import types


from datetime import datetime, timedelta
from telebot import types

def create_event(tgbot, call):
    markup = types.InlineKeyboardMarkup(row_width=5)  # Устанавливаем row_width в 5
    start_date = datetime.now()
    days = []

    # Заполнение списка датами на 30 дней вперед
    for i in range(30):
        day = start_date + timedelta(days=i)
        days.append(day.strftime('%Y-%m-%d'))

    taked_days = {'datetime': '2024-09-23'}  # Запрос к БД на наличие занятых дней за период в 30 дней

    buttons = []
    for day in days:
        _day = day.split('-')[2]
        if day in taked_days.values():
            buttons.append(types.InlineKeyboardButton("⭕" + _day, callback_data=f"create_event_day {day}"))
        else:
            buttons.append(types.InlineKeyboardButton(_day, callback_data=f"create_event_day {day}"))

    # Добавляем кнопки в разметку по 5 в ряд
    for i in range(0, len(buttons), 5):
        markup.add(*buttons[i:i+5])

    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите дату:", reply_markup=markup)
    except:
        tgbot.send_message(call.message.chat.id, "Выберите дату:", reply_markup=markup)

def choice_time(tgbot, call):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Начальная дата - текущий день
    start_date = datetime.now()
    # Список для хранения дат
    times = []
    # Заполнение списка датами на 30 дней вперед
    for i in range(30):
        day = start_date + timedelta(hours=i)
        days.append(day.strftime('%h '))

    taked_days = {'datetime': '2024-09-23'}# Запрос к БД на наличие занятых дней за период в 30 дней

    for day in days:
        _day = day.split('-')[2]
        if day in taked_days.values():
            markup.add(types.InlineKeyboardButton("⭕" + _day, callback_data=f"create_event_day {day}"))
        else:
            markup.add(types.InlineKeyboardButton(_day, callback_data=f"create_event_day {day}"))

    #except Exception as e:
        #print(e)
    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Выберите дату:", reply_markup=markup)
    except:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Выберите дату:", reply_markup=markup)
