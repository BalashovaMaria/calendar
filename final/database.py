import sqlite3
import os


class BaseHandler:
    def __init__(self, path):
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
        for time in times:
            s = f"INSERT INTO RECORDS(name, dosage, time, date) VALUES('{name}','{dosage}','{time}','{date}')"
            self._cur.execute(s)
        self._conn.commit()

    def find(self, date):
        self._cur.execute(f"SELECT * FROM RECORDS WHERE date = '{date}';")
        return self._cur.fetchall()

    def get_all(self):
        self._cur.execute(f"SELECT * FROM RECORDS;")
        return self._cur.fetchall()

    def delete(self, date, time=None):
        if time:
            self._cur.execute(f"DELETE FROM RECORDS WHERE date = '{date}' AND time = '{time}';")
        else:
            self._cur.execute(f"DELETE FROM RECORDS WHERE date = '{date}';")
        self._conn.commit()
