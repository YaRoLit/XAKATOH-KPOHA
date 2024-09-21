import settings
import temporaryStorage
import temporaryStorage
import schedule
import time
from telebot import types

from users import Users


def adminNotify(tgbot, id, datetime, long, event_type, city, place, tags, event_name, description, creator, speakers, event_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    time = str(datetime).split()[1]
    markup.add(types.InlineKeyboardButton("✅", callback_data=f"wait_event_accept {id} {event_id}"), types.InlineKeyboardButton("❌", callback_data=f"wait_event_decline {id} {event_id} {time}"))
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
        print(settings.msgs[id]['msgss'])
    settings.msgs[id]['creator'] = creator
    print(settings.msgs[id]['creator'])

def adminDecline(tgbot, call, id, name):
    admin_name = call.from_user.username
    if int(id) not in settings.msgs:
            settings.msgs[id] = {}
            settings.msgs[id]['msgss'] = []
    for msg in settings.msgs[id]['msgss']:
        tgbot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Заявка о проведении события #{name} отклонена @{admin_name} ❌")
        settings.msgs[id]['msgss'].remove(msg)

    tgbot.send_message(settings.msgs[id]['creator'], f"Заявка о проведении события #{name} отклонена. Администратор: @{admin_name} ❌")
    temporaryStorage.createEvent.dismisEvent(id)

def adminAccept(tgbot, call, id, name, time):
    id = int(id)
    admin_name = call.from_user.first_name

    if int(id) not in settings.msgs:
            settings.msgs[id] = {}
            settings.msgs[id]['msgss'] = []
    print(settings.msgs[id]['msgss'])
    for msg in settings.msgs[id]['msgss']:
        tgbot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Заявка о проведении события #{name} принята @{admin_name} ✅")
        
    for i in range(len(settings.msgs[id]['msgss'])-1):
        settings.msgs[id]['msgss'].remove(settings.msgs[id]['msgss'][i])

    tgbot.send_message(settings.msgs[id]['creator'], f"Заявка о проведении события #{name} одобрена. Администратор: @{admin_name} ✅")
    temporaryStorage.createEvent.acceptEvent(id)
    schedule_event(tgbot, time, call)
    #notify_all(speakers, datetime, long, event_type, city, place, tags, event_name, description, event_id)
    
    
def schedule_event(tgbot, event, call):
    #удаление события по тегу
    schedule.clear(str(event))
    # Переработка времени по сдвигу (delay)
    timeWithDelay: str
    checkMin = int(str(event).split(':')[1]) - settings.delay
    checkHour = int(str(event).split(':')[0])
    if checkMin < 10 and checkMin >=0:
        timeWithDelay = f'{str(checkHour)}:0{str(checkMin)}'
    elif checkMin < 0:
        timeWithDelay = f'{str(checkHour - 1)}:{str(60 - settings.delay)}'
    else:
        timeWithDelay = f'{str(checkHour)}:{str(checkMin)}'

    schedule.every().day.at(timeWithDelay).do(send_msg, tgbot, call).tag(str(event))

#это запускаем в отдельный поток в ГЛАВНОЙ сцене!!!!
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
        
def send_msg(tgbot, call):
    tgbot.send_message(call.message.chat.id, 'Круто')
    #temporaryStorage.createEvent.acceptEvent(id)
    
def notify_all(tgbot, speakers, datetime, long, event_type, city, place, tags, event_name, description, event_id):
    users = Users()
    
    chat_ids = set()
    tag_list = tags.split('#')[1:]
    for tag in tag_list:
        users_list = users.find_by_tag(tag).user_id.to_list()
        chat_ids.update(users_list)
    
    for chat_id in chat_ids:
        tgbot.send_message(chat_id, 
f"""Новое событие: {event_type} \"{event_name}\".
{datetime.strftime("%d/%m/%Y")} в {datetime.strftime("%H:%M")}

{description}

Спикеры: {speakers};
Длительность: {long};
Место: {city}, {place};
Теги: {tags}.
""")
        
        
