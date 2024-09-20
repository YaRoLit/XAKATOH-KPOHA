import sqlite3


class DbCheck:

    @staticmethod
    def createDB(name='test.sql'):
        con = sqlite3.connect(name)
        cur = con.cursor()

        # Создание таблицы, если она не существует
        cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, data TEXT, tags TEXT, accept TEXT)')
        con.commit()

        # Данные для вставки
        data = [
            {"id": 0, "data": "18:00", "tags": "#Chat", "accept": "None"},
            {"id": 1, "data": "12:00", "tags": "#tag", "accept": "None"},
            {"id": 2, "data": "14:00", "tags": "#pupa", "accept": "None"},
            {"id": 3, "data": "18:00", "tags": "#lupa", "accept": "None"},
        ]

        # Вставка данных
        cur.executemany("INSERT INTO users (id, data, tags, accept) VALUES (:id, :data, :tags, :accept)", data)
        con.commit()

        cur.close()
        con.close()

    @staticmethod
    def acceptEvent(time: str, idUser: int):
        con = sqlite3.connect("test.sql")
        cur = con.cursor()

        # Получаем всех пользователей
        cur.execute("SELECT * FROM users")
        idUsersList = cur.fetchall()

        # Обновляем статус пользователей
        for user in idUsersList:
            if user[1] == time and user[0] != idUser:
                cur.execute('UPDATE users SET accept = ? WHERE id = ?', ("False", user[0]))

        # Устанавливаем статус для текущего пользователя
        cur.execute('UPDATE users SET accept = ? WHERE id = ?', ("True", idUser))

        con.commit()
        cur.close()
        con.close()

    @staticmethod
    def checkDB(name=None):
        con = sqlite3.connect("test.sql")
        cur = con.cursor()

        # Вывод всех пользователей
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.close()
        con.close()


DbCheck.createDB()
DbCheck.acceptEvent("18:00", 3)
DbCheck.checkDB()
