import sqlite3
import db.connection as connection


conn = connection.conn
def registration(tg_id, conn=conn):
    sql_core = """INSERT INTO users values (?)"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (tg_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def add_task(task_name, deadline, user_id, conn=conn):
    sql_core = """INSERT INTO tasks (task_name, deadline, status, user_id)values (?,?,?,?)"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (task_name, deadline, 0, user_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False