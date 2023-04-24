import logging

from database import connect
from models import Genre
import asyncio

async def add_genre(genre: Genre, book_id: int = None) -> None:
    if not genre: return
    connection = await connect()
    query = "INSERT INTO genre(id, parent_id, title, books_count, url) VALUES($1, $2, $3, $4, $5)"
    try:
        await connection.execute(query, genre.Id, genre.ParentId, genre.Title, genre.BooksCount, genre.Url)
        logging.info(f"Успешно сохранили жанр: {genre.Title}")
    except BaseException as err:
        logging.info(f"Ошибка-postgres: {err}")
    finally:
        await connection.close()
        if book_id:
            await set_connection_between_book_and_genre(book_id, genre.Id)


async def check_genre_exist(genre_id: int) -> bool:
    connection = await connect()
    query = f"SELECT id FROM genre WHERE id={genre_id}"
    exists = await connection.fetchrow(query)
    await connection.close()
    
    if exists:
        logging.info(f"Жанр {genre_id} существует.")
        return True
    return False


async def set_connection_between_book_and_genre(book_id: int, genre_id: int):
    connection = await connect()
    query = "INSERT INTO book_genre(book_id, genre_id) VALUES($1, $2)"
    try:    
        await connection.execute(query, book_id, genre_id)
        logging.info(f"Успешно проставили связь между книгой и жанром [{book_id}:{genre_id}]")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        await connection.close()