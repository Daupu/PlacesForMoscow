import sqlite3
from aiogram import types


class DATABase:
    def __init__(self):
        self.conn = sqlite3.connect('data_base.db')
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS person 
            (id_person INTEGER UNIQUE,name_person TEXT,person_last_name TEXT,person_username TEXT,is_bot TEXT)
            """)

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS answer 
            (id_person INTEGER,name_person TEXT,person_last_name TEXT,person_username TEXT,person_answer TEXT) 
            """)

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS information 
            (info_name TEXT UNIQUE,info_text TEXT) 
            """)
        self.conn.commit()

    def data_add_new_person(self):
        user = types.User.get_current()
        id_person = user.id
        name_person = user.first_name
        person_last_name = user.last_name
        person_username = user.username
        is_bot = user.is_bot
        self.c.execute("""
        INSERT OR REPLACE INTO person
        VALUES (?,?,?,?,?)""", (id_person, name_person, person_last_name, person_username, is_bot))
        self.conn.commit()

    def data_add_text_person(self, person_answer):
        user = types.User.get_current()
        id_person = user.id
        name_person = user.first_name
        person_last_name = user.last_name
        person_username = user.username
        self.c.execute("""
        INSERT INTO answer
        VALUES (?,?,?,?,?)""", (id_person, name_person, person_last_name, person_username, person_answer))
        self.conn.commit()

    def data_add_info_text(self, info_name, info_text):
        self.c.execute("""
        INSERT INTO information
        VALUES (?,?)""", (info_name, info_text))
        self.conn.commit()

    def data_update_info(self, info_name, info_text):
        self.c.execute("UPDATE information SET info_text = ?  WHERE info_name = ?", (info_text,info_name))
        self.conn.commit()

    def data_info_return(self, info_name, limit: int = 1):
        self.c.execute("""SELECT info_text  FROM information WHERE info_name = ? 
        ORDER BY info_name DESC LIMIT ?""", (info_name, limit))
        res = self.c.fetchone()
        return res[0]

    def data_return_all_info(self):
        self.c.execute("""SELECT * FROM answer """)
        res = self.c.fetchall()
        return res

    def data_delete_person(self):
        self.c.execute("""
        DROP TABLE IF EXISTS person
        """)
        self.conn.commit()

    def data_delete_answer(self):
        self.c.execute("""
        DROP TABLE IF EXISTS answer
        """)
        self.conn.commit()

    def data_delete_information(self):
        self.c.execute("""
        DROP TABLE IF EXISTS information
        """)
        self.conn.commit()


"""
work = DATABase()
work.data_return_all_info()
"""
