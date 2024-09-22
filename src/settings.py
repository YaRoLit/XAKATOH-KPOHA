from scheduler import Scheduler
from users import Users

TELEGRAM_TOKEN = '7221735219:AAHacKjwFbTr8w95_qaHDR6xHtF85V6GoHw'
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