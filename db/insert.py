import psycopg2
import db.connection as connection

conn = connection.conn


def registration(tg_id, conn=conn):
    sql_core = """INSERT INTO users VALUES (%s)"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (tg_id,))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(e)
        return False


def add_task(task_name, deadline, user_id, conn=conn):
    sql_core = """INSERT INTO tasks (task_name, deadline, status, user_id) VALUES (%s, %s, %s, %s)"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (task_name, deadline, 0, user_id))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(e)
        return False