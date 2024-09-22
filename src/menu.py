import settings
import importlib
from telebot import types
from telebot.apihelper import ApiTelegramException
from users import Users

events = settings.events
users = settings.users
cities = settings.cities
tags = settings.tags

def update_settings():
    global events
    global users
    global cities
    global tags
    settings.cities = cities
    settings.events = events
    settings.users = users
    settings.tags = tags
    importlib.reload(settings)

def tag_select(tgbot, call, uid):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    for tag in tags:
        if tag in str(users.show_user_tags(str(uid))): #ЗАПРОС К БД
            markup.add(types.InlineKeyboardButton("✅ " + tag, callback_data=f"tag_to_user_remove {tag}"))
        else:
            markup.add(types.InlineKeyboardButton(tag, callback_data=f"tag_to_user_add {tag}"))

    markup.add(types.InlineKeyboardButton("Готово", callback_data=f"to_main_menu"))
    #except Exception as e:
        #print(e)
    try:
        tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Что вас интересует?", reply_markup=markup)
    except Exception as e:
        print(e)
        extra(tgbot, call, markup)
    
def extra(tgbot, call, markup):
    try:
        tgbot.send_message(call.message.chat.id, f"Что вас интересует?", reply_markup=markup)
    except:
        tgbot.send_message(call.chat.id, f"Что вас интересует?", reply_markup=markup)

def main_menu(tgbot, call):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    plan = types.InlineKeyboardButton("🚀 Запланировать", callback_data="create_event")
    calendar = types.InlineKeyboardButton("📅 События", callback_data="calendar")
    tags = types.InlineKeyboardButton("🏷 Мои интересы", callback_data="to_tag_menu")

    markup.add(calendar)
    markup.add(plan)
    markup.add(tags)

    #except Exception as e:
        #print(e)
    gif_path = 'assets/krona.mp4'  # Замените на путь к вашему локальному файлу
    with open(gif_path, 'rb') as gif:
        try:
            tgbot.send_video(chat_id=call.message.chat.id, video=gif, caption=f"Добро пожаловать, {call.from_user.first_name}. \n\nГлавное меню:", reply_markup=markup)
        except Exception as e:
            print(e)
            tgbot.send_video(chat_id=call.chat.id, video=gif, caption=f"Добро пожаловать, {call.from_user.first_name}. \n\nГлавное меню:", reply_markup=markup)


def ai_approval_menu(tgbot, message, action, time, date, place, length, event_type):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚫 Отменить", callback_data="voice_undo"),
        types.InlineKeyboardButton("✅ Подтвердить", callback_data="voice_approve"))

    if(action == 'add'): action_message = 'запланировать'
    if(action == 'remove'): action_message = 'отменить'
    
    tgbot.send_message(chat_id=message.chat.id, 
                       text=f'Вы хотите {action_message} событие?\nМесто: {place}\nВремя: {time[0:5]}\nДата: {date}\nДлительность: {length} минут\nНазначение: {event_type}',
                       reply_markup=markup)
    
    
def voice_approve_button(tgbot, message):
    # TODO: вызвать планировщика
    tgbot.delete_message(message.chat.id, message.message_id)
    
def voice_undo_button(tgbot, message):
    tgbot.delete_message(message.chat.id, message.message_id)
    