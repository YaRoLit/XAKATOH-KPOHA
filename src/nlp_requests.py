from time import strftime
from menu import ai_approval_menu
from response import emptyCalendar_message, render_eventlist, valueError_message
import settings
from transcribator import Transcribator
from scheduler import Scheduler

def error_action(tgbot, message):
    tgbot.send_message(chat_id=message.chat.id, text=valueError_message())
    return

def search_action(tgbot, message, args):
    sc = Scheduler()
    
    month = args[1][0]
    day = args[1][1]
    year = args[1][2]
    
    df = sc.show_day(year, month, day)
    
    events_on_day = settings.events.show_day(year, month, day)
    
    if not events_on_day.empty:
        text = f"События на {year}-{month:02d}-{day:02d}:\n"
        for _, event in events_on_day.iterrows():
            text += f"- {event['event_name']} ({event['event_type']}) в {event['datetime'].strftime('%H:%M')}\n"
    else:
        text = f"На {year}-{month:02d}-{day:02d} нет запланированных событий."
        
    # tgbot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=call.message.reply_markup)
    
    tgbot.send_message(chat_id=message.chat.id, text=text)

    # text = #render_eventlist(df)
    # joint_text = '\n'.join(text)
    
    # if(not joint_text):
    #     tgbot.send_message(chat_id=message.chat.id, text=emptyCalendar_message(day, month, year))
    # else:
    #     tgbot.send_message(chat_id=message.chat.id, text=joint_text)
    
    return

def add_action(tgbot, message, args):
    action = args[0]
    date = '.'.join([str(x) for x in args[1]])
    time = ':'.join([str(x) for x in args[2]])
    place = args[3]
    duration = args[4]
    event_type = args[5]
        
    ai_approval_menu(tgbot, message, action, time, date, place, duration, event_type)
        
    return

def remove_action(tgbot, message, args):
    date = '.'.join(args[1])
    time = ':'.join(args[2])
    place = args[2]
    
    return

def nlp_request(tgbot, message, text):
    tr = Transcribator()
    args = tr.request_preprocessing(text)
    
    action = args[0]
    
    if(action == 'error'):        
        error_action(tgbot, message)
    elif(action == 'search'):
        search_action(tgbot, message, args)
    elif(action == 'add'):
        add_action(tgbot, message, args)
    elif(action == 'remove'):
        remove_action(tgbot, message, args)