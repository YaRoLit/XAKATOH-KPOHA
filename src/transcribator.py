import datetime
import speech_recognition as sr
from transformers import pipeline


class Transcribator:
    def __init__(self) -> None:
        self.rec = sr.Recognizer()
        self.qa_model = pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2")
    

    def transcribe(self, audiofile) -> list:
        '''Транскрибация аудиофайла (перевод в текст)'''
        with sr.AudioFile(audiofile) as source:
            audio = self.rec.record(source)
            try:
                text = self.rec.recognize_google(audio, language="ru-RU")
                return text
            except Exception:
                return ['Error']


    def request_preprocessing(self, text: str) -> list:
        '''Обработка и формализация пользовательского запроса'''
        try:
            date = self.parse_date(text=text)
        except:
            return ['error']
        time = self.parse_time(text=text)
        duraton = self.parse_duration(text=text)
        place = self.parse_place(text=text)
        e_type = self.parse_event_type(text=text)
        event_type_answer = self.qa_model(question="Что нужно сделать?", context=text)['answer'].strip()
        plane_sinonyms = ["забронир", "созд", "запланир", "организ", "сдел"]
        for sinonim in plane_sinonyms:
            if sinonim in event_type_answer:
                return ['add', date, time, place, duraton, e_type]
        rm_sinonyms = ["удал", "убер", "убр", "отмен", "очист"]
        for sinonim in rm_sinonyms:
            if sinonim in event_type_answer:
                return ['remove', date, time, place]
        show_events_sinonyms = ["покаж", "посм", "вывед", "какие", "планы", "календар"]
        for sinonim in show_events_sinonyms:
            if sinonim in event_type_answer:
                return ['search', date]
        return ['error']


    def parse_place(self, text: str) -> str:
        '''Поиск указания локации в запросе'''
        place = self.qa_model(question="О каком месте идет речь?", context=text)['answer'].strip()
        if "переговор" in place:
            return "комната для переговоров"
        elif "зал" in place:
            return "большой зал"
        else:
            return "комната для переговоров"


    def parse_event_type(self, text: str) -> str:
        '''Поиск указания типа встречи в запросе'''
        event_type = self.qa_model(question = "О каком событии идет речь?", context=text)['answer'].strip()
        if "кругл" in event_type:
            return "круглый стол"
        elif "индив" in event_type:
            return "индивидуальная встреча"
        elif "отрасл" in event_type:
            return "отраслевая встреча"
        elif "открыт" in event_type:
            return "открытая встреча"
        else:
            return "индивидуальная встреча"


    def parse_duration(self, text: str) -> int:
        '''Поиск указания длительности встречи в запросе и парсинг в минуты'''
        long = self.qa_model(question="Какова длительность события?", context=text)['answer'].strip()
        numbers = ''.join(c if c.isdigit() else ' ' for c in long).split()
        if "час" in long:
            return int(numbers[0]) * 60
        elif "мин" in long:
            return int(numbers[0])
        else:
            return 30


    def parse_time(self, text: str) -> list:
        '''Поиск именованной сущности время в запросе'''
        time = self.qa_model(question="О каком времени идет речь?", context=text)['answer'].strip()
        time = ''.join(c if c.isdigit() else ' ' for c in time).split()
        if len(time) == 1:
            time.append('00')
        return time

    def parse_date(self, text: str) -> list:
        '''Поиск именованной сущности дата в запросе'''
        date = self.qa_model(question="О какой дате идет речь?", context=text)['answer'].strip()
        today = datetime.datetime.now()
        if "сегодн" in date:
            return [today.month, today.day, today.year]
        elif "послезавтр" in date:
            today_plus = (today + datetime.timedelta(days=2))
            return [today_plus.month, today_plus.day, today_plus.year]
        elif "завтр" in date:
            today_plus = (today + datetime.timedelta(days=1))
            return [today_plus.month, today_plus.day, today_plus.year]
        date = date.split()
        try:
            day = int(date[0])
        except ValueError:
            day = today.day
        if len(date) > 1:        
            month = self.transform_month(month=date[1])
        else:
            month = today.month
        if len(date) > 2:
            try:
                year = int(date[2])
            except ValueError:
                pass
        else:
            year = today.year     
        return [month, day, year]


    def transform_month(self, month: str) -> int:
        '''Перевод названий месяцев в их числовую форму'''
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
            return datetime.datetime.now().month

