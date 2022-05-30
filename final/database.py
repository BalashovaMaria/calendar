import sqlite3
import os

# Класс для создания базы данных
class BaseHandler:
    def __init__(self, path):
        # Создает таблицу под названием 'records' для записи в нее данных, создаются столбцы текстового формата для распределения данных в них
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self._path = os.path.join(BASE_DIR, path)
        if not os.path.exists(self._path):
            self._conn = sqlite3.connect(self._path)
            self._cur = self._conn.cursor()
            self._cur.execute("CREATE TABLE RECORDS(name TEXT , dosage TEXT, time TEXT, date TEXT)")
            self._cur.execute("CREATE INDEX new_ind ON RECORDS(date)")
            self._conn.commit()
        else:
            self._conn = sqlite3.connect(self._path)
            self._cur = self._conn.cursor()

    def add_record(self, name: str, dosage: str, times: list, date: str):
        # Добавляет данные в таблицу 'records'
        for time in times:
            s = f"INSERT INTO RECORDS(name, dosage, time, date) VALUES('{name}','{dosage}','{time}','{date}')"
            self._cur.execute(s)
        self._conn.commit()

    def find(self, date):
        # Находит соответствующую дату для запроса записей соответствующих данных
        self._cur.execute(f"SELECT * FROM RECORDS WHERE date = '{date}';")
        return self._cur.fetchall()

    def get_all(self):
        # Передает сохраненные данные из базы данных в дочернее окно при последующих его вызовах
        self._cur.execute(f"SELECT * FROM RECORDS;")
        return self._cur.fetchall()

    def delete(self, date, time=None):
        if time:
            self._cur.execute(f"DELETE FROM RECORDS WHERE date = '{date}' AND time = '{time}';")
        else:
            self._cur.execute(f"DELETE FROM RECORDS WHERE date = '{date}';")
        self._conn.commit()
