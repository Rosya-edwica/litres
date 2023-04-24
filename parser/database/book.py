import logging

from database import connect
from models import Book


def add_book(book: Book) -> None:
    if not book: return
    connection = connect()
    cursor = connection.cursor()
    
    query = """INSERT INTO book(id, title, description, language, final_price, full_price, currency, min_age, rating, year, image, url, pages, is_audio) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(query, (book.Id, book.Title, book.Description, book.Language, book.Price.FinalPrice, book.Price.FullPrice,
            book.Price.Currency, book.MinAge, book.Rating, book.Year, book.Image, book.Url, book.Pages, book.IsAudio))

        connection.commit()
        logging.info(f"Успешно сохранили книгу: {book.Title}")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        connection.close()
        

def check_book_exist(book_id: int) -> bool:
    connection = connect()
    cursor = connection.cursor()
    query = f"SELECT id FROM book WHERE id={book_id}"
    cursor.execute(query)
    exists = cursor.fetchone()
    connection.close()
    
    if exists:
        logging.info(f"Книга {book_id} существует.")
        return True
    return False       


def set_connection_between_book_and_genre(book_id: int, genre_id: int):
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO book_genre(book_id, genre_id) VALUES(%s, %s)"
    try:    
        cursor.execute(query, (book_id, genre_id))
        connection.commit()
        logging.info(f"Успешно проставили связь между книгой и жанром [{book_id}:{genre_id}]")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        connection.close()


def set_connection_between_book_and_author(book_id: int, author_id: int):
    connection = connect()
    cursor = connection.cursor()
    query = "INSERT INTO book_author(book_id, author_id) VALUES(%s, %s)"
    try:
        cursor.execute(query, (book_id, author_id))
        connection.commit()
        logging.info(f"Успешно проставили связь между книгой и автором [{book_id}:{author_id}]")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        connection.close()