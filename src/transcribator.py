import speech_recognition as sr
from dateutil import parser
from datetime import datetime
import subprocess


class Transcribator:
    def __init__(self) -> None:
        self.rec = sr.Recognizer()
    
    def transcribe(self, audiofile) -> list:
        subprocess.call(['ffmpeg', '-i', f'./audio/{audiofile}', './audio/tmp.wav'])
        with sr.AudioFile('./audio/tmp.wav') as source:
            audio = self.rec.record(source)
            try:
                text = self.rec.recognize_google(audio, language="ru-RU")
                return text.split()
            except Exception:
                return ['Error']
    
    def events_type_recognize(self, text: list) -> dict:
        event = {}
        if "покажи" in text:
            if "сегодня" in text:
                pass
            if "неделю" in text:
                pass
            if "месяц" in text:
                pass
        elif "запланируй" in text:
            event_datetime = self.keywords_finder(text=text)
            event_datetime = parser.parse(f"{event_datetime['month']} {event_datetime['day']} {event_datetime['year']} {event_datetime['time']}")
            event['event_type'] = text[text.index("запланируй") + 1]
            event['place'] = text[text.index("место") + 1]  
            event['datetime'] = event_datetime
            return event
        elif "отмени" in text:
            event_datetime = self.keywords_finder(text=text)
            event_datetime = parser.parse(f"{event_datetime['month']} {event_datetime['day']} {event_datetime['year']} {event_datetime['time']}")
            event['event_type'] = text[text.index("отмени") + 1]
            event['place'] = text[text.index("место") + 1]
            event['datetime'] = event_datetime
            return event

    def keywords_finder(self, text: list) -> dict:
        keywords = {}
        keywords['time'] = text[text.index("время") + 1]
        keywords['day'] = text[text.index("дата") + 1]
        keywords['month'] = text[text.index("дата") + 2]
        keywords['month'] = self.transform_month(keywords['month'])
        keywords['year'] = text[text.index("дата") + 3]
        return keywords

    def transform_month(self, month: str) -> str:
        if "январ" in month:
            return 1
        elif "феврал" in month:
            return 2
        elif "март" in month:
            return 3        
        elif "апрел" in month:
            return 4
        elif "ма" in month:
            return 5
        elif "июн" in month:
            return 6
        elif "июл" in month:
            return 7
        elif "август" in month:
            return 8
        elif "сентябр" in month:
            return 9
        elif "октябр" in month:
            return 10
        elif "ноябр" in month:
            return 11
        elif "декабр" in month:
            return 12
        else:
            return str(datetime.now().month)

