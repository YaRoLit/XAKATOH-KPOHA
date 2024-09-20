#бот с использованием этой биюлиотеки
import telebot
import schedule
import time
import threading

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

jobs = {}

def check_job(chat_id):
    bot.send_message(chat_id, 'Время для события!')

# создание события /add_event время (формат 18:00)
#добавить функцию удаления события (del jobs[chat_id])
@bot.message_handler(commands=['add_event'])
def add_event(message):
    chat_id = message.chat.id
    time_str = message.text.split()[1]

    if chat_id in jobs:
        bot.send_message(chat_id, 'У вас уже есть запланированное событие.')
        return
    #это добавляет событие на указанное время и вызывает функцию check_job
    schedule.every().day.at(time_str).do(check_job, chat_id)

    jobs[chat_id] = time_str
    bot.send_message(chat_id, f'Событие добавлено на {time_str}')


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=run_scheduler).start()
    bot.polling(none_stop=True)
