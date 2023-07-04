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


    def create_table_admins_chat(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS admins_chat
                (chat_id BIGINT PRIMARY KEY,
                is_free BOOLEAN DEFAULT TRUE
                )"""
            )

    def create_table_cache(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS cache
                (user_id BIGINT PRIMARY KEY,
                admin_chat_id BIGINT,
                tag TEXT,
                date_open DATETIME,
                date_close DATETIME)
            """
            )

    def create_table_statistic(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS statistic
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                time TEXT
                )
            """
            )

    def add_admin_chat_ids(self, admin_chat_id):
        with self.connection:
            self.admin_chat_id = admin_chat_id
            query = "INSERT INTO admins_chat (chat_id) VALUES (?)"
            self.cursor.execute(query, (admin_chat_id,))
            self.connection.commit()


    def choose_free_admin_chat(self):
        try:
            with self.connection:        
                query = "SELECT chat_id FROM admins_chat WHERE is_free=TRUE"
                self.cursor.execute(query)

                return int(*(self.cursor.fetchall()[0]))
        except IndexError:
            raise NotFreeChatsException


    def change_admin_chat_status_to_not_free(self, chat_id):
        with self.connection:
            self.chat_id = chat_id
            query = f"UPDATE admins_chat SET is_free = FALSE WHERE chat_id = {chat_id}"
            self.cursor.execute(query)
            self.connection.commit()

    def change_admin_chat_status_to_free(self, chat_id):
        with self.connection:
            self.chat_id = chat_id
            query = f"UPDATE admins_chat SET is_free = TRUE WHERE chat_id = {chat_id}"
            self.cursor.execute(query)
            self.connection.commit()


    

    def save_data_to_cache(self, user_id, adm_chat_id, tag, date_open):
        with self.connection:
            self.tag = tag
            self.user_id = user_id
            self.admin_chat_id = adm_chat_id
            self.date_open = date_open

            query = "INSERT INTO cache (user_id, admin_chat_id, tag, date_open) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (user_id, adm_chat_id, tag, date_open,))
            self.connection.commit()

    def select_tag_from_cache(self, user_id):
        with self.connection:
            self.user_id = user_id            
            query = f"SELECT tag FROM cache WHERE user_id={user_id}"
            self.cursor.execute(query)
            return str(*(self.cursor.fetchall()[0]))
    
    def select_user_id_from_cache(self, chat_id):
        with self.connection:
            self.chat_id = chat_id            
            query = f"SELECT user_id FROM cache WHERE admin_chat_id={chat_id}"
            self.cursor.execute(query)
            return int(*(self.cursor.fetchall()[0]))
        
    def select_date_open_from_cache(self, user_id):
        with self.connection:
            self.user_id = user_id            
            query = f"SELECT date_open FROM cache WHERE user_id={user_id}"
            self.cursor.execute(query)
            return datetime.datetime.strptime((str(*(self.cursor.fetchall()[0])) ), '%Y-%m-%d %H:%M:%S')   
        

    def create_table_statistic(self):
        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS statistic
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                time TEXT
                )
            """
            )

    def save_data_to_statistic(self, tag, time):
        with self.connection:
            self.time = time
            self.tag = tag         

            query = "INSERT INTO statistic (tag, time) VALUES (?, ?)"
            self.cursor.execute(query, (tag, time))
            self.connection.commit()        
















    