import settings
import temporaryStorage
from users import Users
import create_event
from datetime import datetime, timedelta
from menu import *
import handle_event

users = settings.users

def handle_msg(tgbot, call):

    if call.data.split(" ", 1)[0] == "tag_to_user_add":
        username = call.from_user.username
        print(str(call.message.chat.id), call.data.split(" ")[1])
        users.add_tag(str(call.message.chat.id), call.data.split(" ")[1])  # ЗАПРОС К БД
        users.bd_save()
        tag_select(tgbot, call, call.message.chat.id)
    elif call.data.split(" ", 1)[0] == "tag_to_user_remove":
        username = call.from_user.username
        users.rm_tag(str(call.message.chat.id), call.data.split(" ")[1])  # ЗАПРОС К БД
        users.bd_save()
        tag_select(tgbot, call, call.message.chat.id)
    elif call.data.split(" ", 1)[0] == "to_main_menu":
        tgbot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        main_menu(tgbot, call)
    elif call.data == "to_tag_menu":
        tgbot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        tag_select(tgbot, call, call.message.chat.id)
    elif call.data == "create_event":
        create_event.event_create_start(tgbot, call)
    elif call.data == "voice_approve":
        voice_approve_button(tgbot, call.message)
    elif call.data == "voice_undo":
        voice_undo_button(tgbot, call.message)
    elif call.data.split(" ")[0] == "create_event_day":
        date = call.data.split(" ")[1]
        create_event.event_create_start(tgbot, call)
    elif call.data.split(" ")[0] == "event_type":
        create_event.handle_event_type(tgbot, call)
    elif call.data.split(" ")[0] == "event_date":
        create_event.handle_event_date(tgbot, call)
    elif call.data.split(" ")[0] == "event_city":
        create_event.handle_event_city(tgbot, call)
    elif call.data.split(" ")[0] == "event_place":
        create_event.handle_event_place(tgbot, call)
    elif call.data.split(" ")[0] == "event_tag":
        create_event.handle_event_tags(tgbot, call)
    elif call.data.split(" ")[0] == "tag_to_event_add":
        tag = call.data.split(" ")[1]
        create_event.handle_event_tags(tgbot, call, tag)
    elif call.data.split(" ")[0] == "tag_to_event_rm":
        tag = call.data.split(" ")[1]
        create_event.handle_event_tags(tgbot, call, '', tag)
    elif call.data == "choose_title":
        create_event.choose_title(tgbot, call)
    elif call.data.split(" ")[0] == "wait_event_accept":
        id = call.data.split(" ")[1]
        time = call.data.split(" ")[3]
        name = call.data.split(" ")[2]
        handle_event.adminAccept(tgbot, call, id, name, time)
    elif call.data.split(" ")[0] == "wait_event_decline":
        id = call.data.split(" ")[1]
        name = call.data.split(" ")[2]
        handle_event.adminAccept(tgbot, call, id, name)
    elif call.data == "empty":
        pass
    else:
        tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)
