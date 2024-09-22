from datetime import datetime, timedelta
import settings
import scheduler
from telebot import types

events = settings.events

def choose_date(tgbot, message):
    markup = types.InlineKeyboardMarkup(row_width=7)
    now = datetime.now()
    start_date = now.replace(day=1)
    week_day = (start_date.weekday())
    days = []

    # Заполнение списка датами на 30 дней вперед
    for i in range(30):
        day = start_date + timedelta(days=i)
        days.append(day.strftime('%Y-%m-%d'))

    buttons = []
    for day in days:
        _day = day.split('-')[2]
        day_date = datetime.strptime(day, '%Y-%m-%d')
        if(day_date.date() == now.date()):
            buttons.append(types.InlineKeyboardButton("📌", callback_data=f"calendar_date {day}"))
        else:
            buttons.append(types.InlineKeyboardButton(_day, callback_data=f"calendar_date {day}"))

    buttons_empty = []
    for i in range(week_day):
        buttons_empty.append(types.InlineKeyboardButton("ㅤ", callback_data=f"empty"))

    days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    days_of_week_buttons = []
    for day in days_of_week:
        days_of_week_buttons.append(types.InlineKeyboardButton(day, callback_data=f"empty"))

    for i in range(0, len(days_of_week_buttons), 7):
        markup.add(*days_of_week_buttons[i:i+7])

    while len(buttons_empty) < 7:
        buttons_empty.append(buttons.pop(0))

    for i in range(0, len(buttons_empty), 7):
        markup.add(*buttons_empty[i:i+7])

    # Добавляем кнопки в разметку по 7 в ряд
    for i in range(0, len(buttons), 7):
        markup.add(*buttons[i:i+7])

    markup.add(types.InlineKeyboardButton("Назад", callback_data=f"to_main_menu"))
    tgbot.delete_message(chat_id=message.message.chat.id, message_id=message.message.message_id)
    tgbot.send_message(chat_id=message.message.chat.id, text="Выберите дату:ㅤㅤㅤㅤ", reply_markup=markup)

def handle_calendar_date(tgbot, call):
    day = call.data.split()[1]
    year, month, day = map(int, day.split('-'))
    events_on_day = events.show_day(year, month, day)
    events_on_day = events_on_day[events_on_day['event_type'] != "Личная встреча"]

    if not events_on_day.empty:
        text = f"События на {year}-{month:02d}-{day:02d}:\n"
        for _, event in events_on_day.iterrows():
            text += f"- {event['event_name']} ({event['event_type']}) в {event['datetime'].strftime('%H:%M')}\n"
    else:
        text = f"На {year}-{month:02d}-{day:02d} нет запланированных событий."

    tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=call.message.reply_markup)
