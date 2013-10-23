import sqlite3


class Model(object):

    def __init__(self, name, db):
        self.name = name
        self.table = name + "s"
        self.database = db

    def all(self):
        conn = splite3.connect(self.database)
        c = conn.cursor()
        c.execute('SELECT * FROM ?', self.table)
        conn.close()

    def find(self, str):
        conn = splite3.connect(self.database)
        c = conn.cursor()
        c.execute(
            'SELECT * FROM ? WHERE ?=?',
            self.table,
            self.primarykey,
            str)
        conn.close()

    def save(self, ha):
        pass

    def migrate():
        pass
