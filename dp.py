import sqlite3


class DB:
    def __init__(self):
        c = sqlite3.connect('dolls.db', check_same_thread=False)
        self.c = c

    def get_connection(self):
        return self.c

    def __del__(self):
        self.c.close()