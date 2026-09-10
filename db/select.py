import sqlite3
import db.connection as connection


conn = connection.conn
def does_the_string_exist(tg_id, conn=conn):
    sql_core = """SELECT * from users where tg_id = ?"""
    therow = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (tg_id,))
        therow = cursor.fetchall()
        print(f'the user {therow} registrated')
    except sqlite3.Error as e:
        print(e)
    if therow:
        return True
    else:
        return False


def task_list(user_id, conn=conn):
    sql_core = """SELECT * FROM tasks where user_id = ?"""
    task_list = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (user_id,))
        task_list = cursor.fetchall()
        for task in task_list:
            print(task)
    except sqlite3.Error as e:
        print(e)
    if task_list:
        return task_list
    else:
        return False