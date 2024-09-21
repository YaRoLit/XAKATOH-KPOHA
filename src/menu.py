import settings
from telebot import types
from telebot.apihelper import ApiTelegramException

users = settings.users
tags = settings.tags

def tag_select(tgbot, call):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    for tag in tags.keys():
        if tag in users[call.from_user.username].tags: #ЗАПРОС К БД
            markup.add(types.InlineKeyboardButton("✅ " + tag, callback_data=f"tag_to_user_remove {tag}"))
        else:
            markup.add(types.InlineKeyboardButton(tag, callback_data=f"tag_to_user_add {tag}"))

    markup.add(types.InlineKeyboardButton("Готово", callback_data=f"to_main_menu"))
    #except Exception as e:
        #print(e)
    try:
        #tgbot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        main = tgbot.send_message(call.chat.id, f"Что вас интересует?", reply_markup=markup)
    except:
        main = tgbot.send_message(call.chat.id, f"Что вас интересует?", reply_markup=markup)

def main_menu(tgbot, call):
    #try:
    markup = types.InlineKeyboardMarkup(row_width=2)
    market = types.InlineKeyboardButton("🚀 Создать", callback_data="create_event")
    wallet = types.InlineKeyboardButton("📅 Календарь", callback_data="calendar")
    markup.add(market, wallet)
                                                                                                                                                # Нереализованный функционал Веб-приложения
                                                                                                                                                #web_app_info = types.WebAppInfo("https://localhost:5000")
                                                                                                                                                #button = types.KeyboardButton(text="Веб-приложение", web_app=web_app_info)
                                                                                                                                                #markup.add(button)
    #except Exception as e:
        #print(e)
    gif_path = '../assets/krona.mp4'  # Замените на путь к вашему локальному файлу
    with open(gif_path, 'rb') as gif:
        try:
            tgbot.send_video(chat_id=call.message.chat.id, video=gif, caption="Главное меню", reply_markup=markup)
        except:
            tgbot.send_video(chat_id=call.message.chat.id, video=gif, caption="Главное меню", reply_markup=markup)

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
    