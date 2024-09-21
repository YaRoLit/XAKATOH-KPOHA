import schedule
import globalVar # для переменной сдвига по времени(для удобства)
import time
def print_e_test(event):
    print("Hello!" + event)

def schedule_event(event):
    #удаление события по тегу
    schedule.clear(str(event['time']))
    # Переработка времени по сдвигу (delay)
    timeWithDelay: str
    checkMin = int(str(event['time']).split(':')[1]) - globalVar.delay
    checkHour = int(str(event['time']).split(':')[0])
    if checkMin < 10 and checkMin >=0:
        timeWithDelay = f'{str(checkHour)}:0{str(checkMin)}'
    elif checkMin < 0:
        timeWithDelay = f'{str(checkHour - 1)}:{str(60 - globalVar.delay)}'
    else:
        timeWithDelay = f'{str(checkHour)}:{str(checkMin)}'

    schedule.every().day.at(timeWithDelay).do(print_e_test, event).tag(str(event['time']))

#это запускаем в отдельный поток в ГЛАВНОЙ сцене!!!!
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)