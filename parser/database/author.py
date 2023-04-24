import logging

from database import connect
from models import Author
import asyncio

async def add_author(author: Author, book_id: int = None) -> None:
    if not author: 
        await asyncio.sleep(0)
        return
    connection = await connect()
    query = "INSERT INTO author(id, fullname, about, books_count, image, url) VALUES($1, $2, $3, $4, $5, $6)"
    try:
        await connection.execute(query, author.Id, author.FullName, author.Description, author.BooksCount, author.Image, author.Url)
        logging.info(f"Успешно сохранили автора: {author.FullName}")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        await connection.close()
        if book_id:
            await set_connection_between_book_and_author(book_id, author.Id)


async def check_author_exist(author_id: int) -> bool:
    connection = await connect()
    query = f"SELECT id FROM author WHERE id={author_id}"
    exists = await connection.fetchrow(query)
    await connection.close()
    
    if exists:
        logging.info(f"Автор {author_id} существует.")
        return True
    return False

async def set_connection_between_book_and_author(book_id: int, author_id: int):
    connection = await connect()
    query = "INSERT INTO book_author(book_id, author_id) VALUES($1, $2)"
    try:
        await connection.execute(query, book_id, author_id)
        logging.info(f"Успешно проставили связь между книгой и автором [{book_id}:{author_id}]")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        await connection.close()