from time import strftime
from menu import ai_approval_menu
from transcribator import Transcribator
from scheduler import Scheduler

def nlp_request(tgbot, message, text):
    tr = Transcribator()
    args = tr.request_preprocessing(text)
    
    action = args[0]
    
    if(action == 'error'):
        return  # TODO error message
    
    if(action == 'search'):
        sc = Scheduler()
        
        month = args[1][0]
        day = args[1][1]
        year = args[1][2]
        
        df = sc.show_day(year, month, day)
        
        return df
    
    date = '.'.join(args[1])
    time = ':'.join(args[2])
    
    if(action == 'add'):
        place = args[3]
        duration = args[4]
        event_type = args[5]
        
    elif(action == 'remove'):
        place = args[2]
    
    
    ai_approval_menu(tgbot, message, action, time, date, place, duration, event_type)