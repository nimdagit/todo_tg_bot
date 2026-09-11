import psycopg2
import db.connection as connection

conn = connection.conn


def delete(task_id, conn=conn):
    sql_core = """DELETE FROM tasks WHERE id = %s"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_core, (task_id,))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(e)
        return False