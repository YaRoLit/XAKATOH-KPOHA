import settings
from user import User
from processes import *
from index import *

tgbot = settings.tgbot

@tgbot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    #try:
    if call.data.split(" ", 1)[0] == "tag_to_user_add":
        username = call.from_user.username
        users[username].tags.append(call.data.split(" ")[1]) #ЗАПРОС К БД
        tag_select(call)
    
    elif call.data.split(" ", 1)[0] == "tag_to_user_remove":
        username = call.from_user.username
        users[username].tags.remove(call.data.split(" ")[1]) #ЗАПРОС К БД
        tag_select(call)
    
    elif call.data.split(" ", 1)[0] == "to_main_menu":
        main_menu(call)

    elif call.data == "create_event":
        tgbot.register_next_step_handler(msg, create_event, tgbot, call)
    
    elif call.data.split(" ")[0] == "create_event_day":
        date = call.data.split(" ")[1]
        

    else:
        tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)


    #except Exception as e:
    #    tgbot.answer_callback_query(callback_query_id=call.id, text="Для авторизации напишите /start", show_alert=True)
    #    print(e)