import sqlite3

from flask import g

db_file = "app.db"

def get_db():
    connection = g.get('db', 'null')
    if connection == 'null':
        try:
            g.db = sqlite3.connect(db_file)
            g.db.row_factory = sqlite3.Row
            return g.db
        except Exception as ex:
            return False
    else:
        return connection
