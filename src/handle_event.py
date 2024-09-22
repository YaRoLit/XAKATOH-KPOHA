import settings
import temporaryStorage
from telebot import types


def adminNotify(tgbot, id, datetime, long, event_type, city, place, tags, event_name, description, creator, speakers, event_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("✅", callback_data=f"wait_event_accept {id} {event_id}"), types.InlineKeyboardButton("❌", callback_data=f"wait_event_decline {id} {event_id}"))
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
    if id not in settings.msgs:
            settings.msgs[id] = {}
            settings.msgs[id]['msgss'] = []
    for msg in settings.msgs[id]['msgss']:
        tgbot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Заявка о проведении события #{name} отклонена @{admin_name} ❌")
        settings.msgs[id].remove(msg)
        settings.msgs[id]['msgss'].remove(msg)

    tgbot.send_message(settings.msgs[id]['creator'], f"Заявка о проведении события #{name} отклонена. Администратор: @{admin_name} ❌")
    createEvent.dismisEvent(id)

def adminAccept(tgbot, call, id, name):
    admin_name = call.from_user.first_name

    if id not in settings.msgs:
            settings.msgs[id] = {}
            settings.msgs[id]['msgss'] = []
    print(settings.msgs[id]['msgss'])
    for msg in settings.msgs[id]['msgss']:
        tgbot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Заявка о проведении события #{name} принята @{admin_name} ✅")
        settings.msgs[id].remove(msg)
        settings.msgs[id]['msgss'].remove(msg)

    tgbot.send_message(settings.msgs[id]['creator'], f"Заявка о проведении события #{name} одобрена. Администратор: @{admin_name} ✅")
    createEvent.acceptEvent(id)