import sqlite3


def conn(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
    return conn

conn = conn(r'.\month_C\todo\db\tasks_and_users.db')