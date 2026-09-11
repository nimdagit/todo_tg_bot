import psycopg2
import db.connection as connection

conn = connection.conn


def does_the_string_exist(tg_id, conn=conn):
    sql_core = """SELECT * FROM users WHERE tg_id = %s"""
    therow = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (tg_id,))
        therow = cursor.fetchall()
        print(f'the user {therow} registrated')
    except psycopg2.Error as e:
        print(e)
    if therow:
        return True
    else:
        return False


def task_list(user_id, conn=conn):
    sql_core = """SELECT * FROM tasks WHERE user_id = %s"""
    task_list = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (user_id,))
        task_list = cursor.fetchall()
        for task in task_list:
            print(task)
    except psycopg2.Error as e:
        print(e)
    if task_list:
        return task_list
    else:
        return False