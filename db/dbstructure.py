import psycopg2
import connection


conn = connection.conn


def create_table(sql, conn=conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print(f"OK: {sql[:40]}...")
    except psycopg2.Error as e:
        print(f"ERROR: {e}")
    return conn


sql_users = """CREATE TABLE IF NOT EXISTS users
    (tg_id BIGINT PRIMARY KEY)
"""

sql_tasks = """CREATE TABLE IF NOT EXISTS tasks
    (id SERIAL PRIMARY KEY,
    task_name TEXT NOT NULL,
    deadline TEXT,
    status INTEGER NOT NULL DEFAULT 0,
    user_id BIGINT REFERENCES users(tg_id)
    )"""

create_table(sql_users)
create_table(sql_tasks)