import sqlite3
import db.connection as connection


conn = connection.conn

def delete(task_id, conn = conn):
    sql_core = """DELETE from tasks where id = ?"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (task_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False