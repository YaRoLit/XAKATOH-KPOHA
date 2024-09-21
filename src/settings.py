from scheduler import Scheduler
from users import Users

TELEGRAM_TOKEN = '8025388311:AAFCIvpE-StyVApOa6bzP3PKYMrQBmpGn8U'
tags = ["Игры", "Деньги"]
users = Users()
events = Scheduler()
cities = {'Saratov': ['Musorka']}
types = ['SexParty']
event_data = {}

global msgs
global lenEvent
global data
global tap
global ev
msgs = {}
ev = {}
tap = 0
lenEvent = 0
data = []

admins = ['1258192437', '480119475']