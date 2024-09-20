from telebot import types
import settings
from user import User
from processes import *
from menu import *

users = settings.users

def handle_msg(tgbot, call):
    #try
    if call.data.split(" ", 1)[0] == "tag_to_user_add":
        username = call.from_user.username
        users[username].tags.append(call.data.split(" ")[1])  # ЗАПРОС К БД
        tag_select(tgbot, call)
    elif call.data.split(" ", 1)[0] == "tag_to_user_remove":
        username = call.from_user.username
        users[username].tags.remove(call.data.split(" ")[1])  # ЗАПРОС К БД
        tag_select(tgbot, call)
    elif call.data.split(" ", 1)[0] == "to_main_menu":
        tgbot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        main_menu(tgbot, call)
    elif call.data == "create_event":
        create_event(tgbot, call)
    elif call.data == "voice_approve":
        voice_approve_button(tgbot, call.message)
    elif call.data == "voice_undo":
        voice_undo_button(tgbot, call.message)
    elif call.data.split(" ")[0] == "create_event_day":
        date = call.data.split(" ")[1]
    else:
        tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)


    #except Exception as e:
    #    tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)
    #    print(e)
