import psycopg2


def connect():
    connection = psycopg2.connect(
        database="litres",
        user="postgres",
        password="admin",
        host="127.0.0.1",
        port=5432
    )
    return connection