import logging

from database import connect
from models import Genre


def add_genre(genre: Genre) -> None:
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO genre(id, parent_id, title, books_count, url) VALUES(%s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (genre.Id, genre.ParentId, genre.Title, genre.BooksCount, genre.Url))
        connection.commit()
        logging.info(f"Успешно сохранили жанр: {genre.Title}")
    except BaseException as err:
        logging.info(f"Ошибка-postgres: {err}")
    finally:
        connection.close()


def check_genre_exist(genre_id: int) -> bool:
    connection = connect()
    cursor = connection.cursor()
    query = f"SELECT id FROM genre WHERE id={genre_id}"
    cursor.execute(query)
    exists = cursor.fetchone()
    connection.close()
    
    if exists:
        logging.info(f"Жанр {genre_id} существует.")
        return True
    return False