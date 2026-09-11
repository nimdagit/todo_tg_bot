import psycopg2
from decouple import config


DATABASE_URL = config('DATABASE_URL')


def get_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print(e)
        return None


conn = get_connection()