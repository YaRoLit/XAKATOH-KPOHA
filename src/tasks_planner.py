import schedule
import time
import threading
import sqlite3
import index
import settings
import scheduler
import datetime

jobs = {}
events = settings.events

class PlannerTask:

    @staticmethod
    def add_task(message, event, nameDB: str = "test.sql"):
        DBevents = sqlite3.connect(nameDB)
        try:
            # Проверяем, существует ли событие с таким же временем
            existing_event = DBevents.execute("SELECT * FROM users WHERE datetime = ?", (event['datetime'],)).fetchall()
            if existing_event:
                print("Событие с таким временем уже существует")
                #tgbot.not_add_event(message)
                settings.ev = existing_event
                return False

            event_time = event['datetime'].split()
            job = schedule.every().day.at(event_time[1]).do(PlannerTask.time_event, event, message)
            jobs[event['datetime']] = job  # Сохраняем ссылку на задачу
            DBevents.execute("INSERT INTO users (datetime, long, event_type, event_id, city, place, tags, event_name, "
                             "description, creator, admin, speakers, quests) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (event['datetime'], event['long'], event['event_type'], event['event_id'], event['city'],
                              event['place'], event['tags'], event['event_name'], event['description'],
                              event['creator'], event['admin'], event['speakers'], event['quests']))
            DBevents.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении задачи: {e}")
        finally:
            DBevents.close()

    @staticmethod
    def replace_task(message, event, nameDB: str = "test.sql"):
        DBevents = sqlite3.connect(nameDB)
        try:
            # Проверяем, существует ли событие с таким ID
            existing_event = DBevents.execute("SELECT * FROM users WHERE event_id = ?", (event['event_id'],)).fetchone()

            if existing_event:
                # Удаляем старое событие из расписания
                existing_datetime = existing_event['datetime']
                existing_datetime = datetime.strptime(existing_datetime)
                events(existing_datetime)  # Отменяем запланированное событие
                del jobs[existing_datetime]  # Удаляем из словаря jobs

            # Запланируем новое событие
            event_time = event['datetime'].split()
            job = schedule.every().day.at(event_time[1]).do(PlannerTask.time_event, event, message)
            jobs[event['datetime']] = job  # Сохраняем ссылку на задачу

            # Обновляем или вставляем новое событие в базу данных
            DBevents.execute("UPDATE users SET datetime = ?, long = ?, event_type = ?, event_id = ?, city = ?, "
                             "place = ?, tags = ?, event_name = ?, description = ?, creator = ?, admin = ?, "
                             "speakers = ?, quests = ? WHERE datetime = ?",
                             (event['datetime'], event['long'], event['event_type'], event['event_id'],
                              event['city'], event['place'], event['tags'], event['event_name'],
                              event['description'], event['creator'], event['admin'],
                              event['speakers'], event['quests'], event['datetime']))

            DBevents.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении/обновлении задачи: {e}")
            return False
        finally:
            DBevents.close()

    @staticmethod
    def time_event(event, message):
        print(event)
        tgbot.notice_event(event, message)
        # вообще тут нужно будет запускать функцию для отправки сообщения всем пользователям с нужными тегами


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
