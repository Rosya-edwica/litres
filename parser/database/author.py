import logging

from database import connect
from models import Author


def add_author(author: Author) -> None:
    if not author: return
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO author(id, fullname, about, books_count, image, url) VALUES(%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (author.Id, author.FullName, author.Description, author.BooksCount, author.Image, author.Url))
        connection.commit()
        logging.info(f"Успешно сохранили автора: {author.FullName}")
    except BaseException as err:
        print(err)
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        connection.close()


def check_author_exist(author_id: int) -> bool:
    connection = connect()
    cursor = connection.cursor()
    query = f"SELECT id FROM author WHERE id={author_id}"
    cursor.execute(query)
    exists = cursor.fetchone()
    connection.close()
    
    if exists:
        logging.info(f"Автор {author_id} существует.")
        return True
    return False