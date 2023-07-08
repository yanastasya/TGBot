import sqlite3
from errors.errors import NotFreeChatsException
import datetime

class DataBase:
    
    #def __init__(self):
        #подключение к базе данных
     #   self.connection = psycopg2.connect(database = 'см. readme',
     #                                      user = 'см. readme',
     ##                                      password = 'см. readme',
     #                                      host = 'см. readme',
    #                                       port = 'см. readme')
     #   self.cursor = self.connection.cursor()

    def __init__(self):        
        self.connection = sqlite3.connect("tg_bot.db", check_same_thread=False)
        self.cursor = self.connection.cursor()


    def create_table_statistic(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS statistic
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                date_open DATETIME,
                date_close DATETIME
                )
            """
            )

    
    def save_data_to_statistic(self, tag, date_open, date_close):
        with self.connection:
            self.tag = tag
            self.date_open = date_open
            self.date_close = date_close         

            query = "INSERT INTO statistic (tag, date_open, date_close) VALUES (?, ?, ?)"
            self.cursor.execute(query, (tag, date_open, date_close))
            self.connection.commit()        
















    