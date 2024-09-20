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
