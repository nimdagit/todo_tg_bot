import sqlite3
import db.connection as connection


conn = connection.conn

def update_status(task_id, conn = conn):
    sql_core = """UPDATE tasks SET status = 1 WHERE id = ?"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (task_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False