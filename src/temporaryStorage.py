import tasks_planner
import scheduler
from telebot import types
import settings
import handler
import handle_event

eventT = {
    'datetime': "2024-09-21 13:00:00",
    'long': "00:30:00",
    'event_type': "Dance",
    'event_id': 0,
    'city': "Novosib",
    'place': "School21",
    'tags': "",
    'event_name': "Tysa",
    'description': "LALALALLALA",
    'creator': "Egor",
    'admin': "-",
    'speakers': "5",
}

# {event: {creator:id, msgss: [msg, msg]}}
msgs = {}

class createEvent:
    data = []

    @staticmethod
    def create_task_in_Storage(datetime: str = "None",
                               long: str = "None",
                               event_type: str = "None",
                               event_id: str = "0",
                               city: str = "None",
                               place: str = "None",
                               tags: str = "None",
                               event_name: str = "None",
                               description: str = "None",
                               creator: str = "None",
                               admin: str = "None",
                               speakers: str = "None",
                               quests: str = "None"):
        event = {
            'datetime': datetime,
            'long': long,
            'event_type': event_type,
            'event_id': event_id,
            'city': city,
            'place': place,
            'tags': tags,
            'event_name': event_name,
            'description': description,
            'creator': creator,
            'admin': admin,
            'speakers': speakers,
            'quests': quests,
            'id': settings.lenEvent,
            'accept': 'None'
        }
        settings.data.append(event)
        settings.lenEvent += 1
        print(settings.lenEvent)
        print("Yes_1")
        return settings.lenEvent

    @staticmethod
    def acceptEvent(tgbot, idevent: int):
        if settings.data is not None:
            for i in settings.data:
                if i['id'] == idevent:
                    try:
                        i.pop('accept')
                        i.pop('id')
                    except:
                        print('Oh shit')
                        pass
                    settings.events.add_event(i)
                    print("Yes_2")
                    handle_event.notify_users(tgbot, i)

    @staticmethod
    def replaceEvent(message, idevent: int, DB: str):
        if settings.data is not None:
            for i in settings.data:
                if i['id'] == idevent:
                    ret = tasks_planner.PlannerTask.replace_task(message, i, DB)
                    print("Yes_5")
                    return ret

    @staticmethod
    def dismisEvent(idevent: int):
        count = 0
        for i in settings.data:
            if i['id'] == idevent:
                settings.data.pop(count)
            count += 1

    @staticmethod
    def getEvent(idevent: int):
        for event in settings.data:
            if event['id'] == idevent:
                return event
        return None
