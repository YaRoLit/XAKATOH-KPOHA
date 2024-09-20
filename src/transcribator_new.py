import speech_recognition as sr
from dateutil import parser
import datetime
from transformers import pipeline


class Transcribator:
    def __init__(self) -> None:
        self.rec = sr.Recognizer()
        self.qa_model = pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2", device='cuda')
    
    def transcribe(self, audiofile) -> list:
        with sr.AudioFile(audiofile) as source:
            audio = self.rec.record(source)
            try:
                text = self.rec.recognize_google(audio, language="ru-RU")
                return text
            except Exception:
                return ['Error']

    def events_type_recognize(self, text: str) -> int:
        event_type_answer = self.qa_model(question="Что нужно сделать?", context=text)['answer'].strip()
        plane_sinonyms = ["забронир", "созд", "запланир", "организ", "сдел"]
        for sinonim in plane_sinonyms:
            if sinonim in event_type_answer:
                return 1
        rm_sinonyms = ["удал", "убер", "убр", "отмен", "очист"]
        for sinonim in rm_sinonyms:
            if sinonim in event_type_answer:
                return 2
        show_events_sinonyms = ["покаж", "посм", "вывед", "какие", "планы"]
        for sinonim in show_events_sinonyms:
            if sinonim in event_type_answer:
                return 3

    def place_recognize(self, text: str) -> str:
        return self.qa_model(question="О каком месте идет речь?", context=text)['answer'].strip()

    def event_type_recognize(self, text: str) -> int:
        if "кругл" in text:
            return 1
        elif "индив" in text:
            return 2
        elif "отрасл" in text:
            return 3
        elif "открыт" in text:
            return 4
        else:
            return 0

    def long_recognition(self, text: str) -> datetime.datetime:
        long = self.qa_model(question="Какова длительность события?", context=text)['answer'].strip()
        numbers = ''.join(c if c.isdigit() else ' ' for c in long).split()
        if "час" in long:
            return int(numbers[0]) * 60
        elif "мин" in long:
            return int(numbers[0])
        else:
            return 30

    def date_recognize(self, text: str) -> datetime.datetime:
        date = self.qa_model(question="О какой дате идет речь?", context=text)['answer'].strip().split()
        day = date[0]
        month = date[1]
        month = self.transform_month(month=month)
        year = str(datetime.datetime.now().year) #year = date[2]
        time = self.qa_model(question="О каком времени идет речь?", context=text)['answer'].strip()
        return parser.parse(f"{month} {day} {year} {time}")

    def transform_month(self, month: str) -> str:
        if "январ" in month:
            return '1'
        elif "феврал" in month:
            return '2'
        elif "март" in month:
            return '3'        
        elif "апрел" in month:
            return '4'
        elif "ма" in month:
            return '5'
        elif "июн" in month:
            return '6'
        elif "июл" in month:
            return '7'
        elif "август" in month:
            return '8'
        elif "сентябр" in month:
            return '9'
        elif "октябр" in month:
            return '10'
        elif "ноябр" in month:
            return '11'
        elif "декабр" in month:
            return '12'
        else:
            return str(datetime.now().month)

