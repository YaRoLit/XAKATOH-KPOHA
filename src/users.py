import pandas as pd
import sqlite3 as sq


class Users:
    def __init__(self, bd_filename='users') -> None:
        self.bd_filename = bd_filename
        conn = sq.connect('{}.sqlite'.format(self.bd_filename))
        self.df = pd.read_sql('select * from {}'.format(self.bd_filename), conn)
        conn.close()
    
    def add_user(self, user_id, tags) -> None:
        '''Добавляем пользователя в БД'''
        self.df.loc[len(self.df)] = {
            'user_id': user_id,
            'tags': tags
            }
    
    def rm_user(self, user_id) -> None:
        '''Удаляем пользователя из БД'''
        self.df = self.df[~(self.df.user_id == user_id)]
    
    def show_users(self) -> pd.DataFrame:
        return self.df
    
    def find_by_tag(self, tag) -> pd.DataFrame:
        return self.df[self.df['tags'].str.contains(tag)]

    def bd_save(self) -> None:
        conn = sq.connect('{}.sqlite'.format(self.bd_filename))
        self.df.to_sql(self.bd_filename, conn, if_exists='replace', index=False)
        conn.close()