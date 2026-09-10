import sqlite3
import connection


conn = connection.conn

def create_table(sql, conn = conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    return conn

sql_tasks = """CREATE TABLE IF NOT EXISTS tasks
    (id integer primary key autoincrement,
    task_name text not null,
    deadline text,
    status integer not null default 0,
    user_id integer references users(tg_id)
    )"""

sql_users = """CREATE TABLE IF NOT EXISTS users
    (tg_id integer primary key)
"""

create_table(sql_users)
create_table(sql_tasks)