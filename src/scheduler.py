import pandas as pd
import datetime
import sqlite3 as sq

# Модуль с базами данных
class Scheduler:
    def __init__(self, bd_filename='events') -> None:
        self.bd_filename = bd_filename
        conn = sq.connect('{}.sqlite'.format("db/" + self.bd_filename))
        self.df = pd.read_sql('select * from {}'.format(self.bd_filename), conn)
        conn.close()
        self.df.datetime = pd.to_datetime(self.df.datetime)


    def show_day(self, year: int, month: int, day: int) -> pd.DataFrame:
        return self.df[(self.df.datetime >= datetime.datetime(year=year, month=month, day=day)) &
                       (self.df.datetime <= datetime.datetime(year=year, month=month, day=(day + 1)))]


    def show_month(self, year: int, month: int) -> pd.DataFrame:
        return self.df[(self.df.datetime >= datetime.datetime(year=year, month=month)) &
                       (self.df.datetime <= datetime.datetime(year=year, month=(month + 1)))]


    def add_event(self, event: dict) -> None:
        self.df.loc[len(self.df)] = event
        self.df = self.df.sort_values(by=['datetime'], ascending=False)

    def rm_event(self, datetime: datetime.datetime, place) -> None:
        self.df = self.df[~((self.df.datetime == datetime) & (self.df.place == place))]

    def bd_save(self) -> None:
        conn = sq.connect('{}.sqlite'.format(self.bd_filename))
        self.df.to_sql(self.bd_filename, conn, if_exists='replace', index=False)
        conn.close()

    def check_datetime(self, date_start: datetime.datetime, long: int) -> pd.DataFrame:
        return self.df[(self.df.datetime >= date_start) &
                       (self.df.datetime <= (date_start + datetime.timedelta(minutes=long)))]

    def check_event(self, place: str, date_start: datetime.datetime, long: int) -> pd.DataFrame:
        return self.df[(self.df.datetime >= date_start) &
                       (self.df.datetime <= (date_start + datetime.timedelta(minutes=long))) &
                       (self.df.place == place)]
