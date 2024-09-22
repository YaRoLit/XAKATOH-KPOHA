import settings
import temporaryStorage
import schedule
import time
from telebot import types
from users import Users

def adminNotify(tgbot, id, datetime, long, event_type, city, place, tags, event_name, description, creator, speakers, event_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    time = str(datetime).split()[1]
    markup.add(types.InlineKeyboardButton("✅", callback_data=f"wait_event_accept {id} {event_id}"),
               types.InlineKeyboardButton("❌", callback_data=f"wait_event_decline {id} {event_id} {time}"))

    for admin in settings.admins:
        msg = tgbot.send_message(admin, (f"Заявка на событие #{event_id}:\n" +
                                         f"Название: {event_name}\n" +
                                         f"Начало: {datetime}\n" +
                                         f"Длительность: {long} минут\n" +
                                         f"Место: {city}, {place}\n" +
                                         f"Спикеры: {speakers}\n" +
                                         f"Описание: {description}\n"), reply_markup=markup)
        if id not in settings.msgs:
            settings.msgs[id] = {}
            settings.msgs[id]['msgss'] = []
        settings.msgs[id]['msgss'].append(msg)
    settings.msgs[id]['creator'] = creator

def adminDecline(tgbot, call, id, name):
    admin_name = call.from_user.username
    if int(id) in settings.msgs:
        for msg in settings.msgs[id]['msgss']:
            tgbot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                    text=f"Заявка о проведении события #{name} отклонена @{admin_name} ❌")
        tgbot.send_message(settings.msgs[id]['creator'], f"Заявка о проведении события #{name} отклонена. Администратор: @{admin_name} ❌")
        del settings.msgs[id]
    temporaryStorage.createEvent.dismisEvent(id)

def adminAccept(tgbot, call, id, name, time):
    id = int(id)
    admin_name = call.from_user.first_name
    if int(id) in settings.msgs:
        for msg in settings.msgs[id]['msgss']:
            tgbot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                    text=f"Заявка о проведении события #{name} принята @{admin_name} ✅")
        tgbot.send_message(settings.msgs[id]['creator'], f"Заявка о проведении события #{name} одобрена. Администратор: @{admin_name} ✅")
        del settings.msgs[id]

    temporaryStorage.createEvent.acceptEvent(tgbot, id)

def notify_users(tgbot, event_type, tags, event_name, datetime, description, speakers, long, city, place, event_id):
    if event_type != "Личная встреча":
        users = Users()
        chat_ids = set()
        tag_list = tags.split('#')[1:]
        for tag in tag_list:
            users_list = users.find_by_tag(tag).user_id.to_list()
            chat_ids.update(users_list)
        for chat_id in chat_ids:
            tgbot.send_message(chat_id, f"""Новое событие: {event_type} \"{event_name}\".
                            {datetime.strftime("%d/%m/%Y")} в {datetime.strftime("%H:%M")}
                            {description}
                            Спикеры: {speakers}
                            Длительность: {long} минут
                            Место: {city}, {place}
                            Теги: {tags}
                            """)

def schedule_event(tgbot):
    scheduler = settings.events
    events = scheduler.df
    for index, event in events.iterrows():
        event_time = event['datetime'] - datetime.timedelta(days=1)
        schedule.every().day.at(event_time.strftime("%H:%M")).do(notify_users, tgbot, event['event_type'], event['tags'],
                                                                 event['event_name'], event['datetime'], event['description'],
                                                                 event['speakers'], event['long'], event['city'], event['place'], event['event_id']).tag(str(event['event_id']))

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
