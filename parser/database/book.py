import logging

from database import connect
from models import Book
import asyncio


async def add_book(book: Book) -> None:
    if not book: 
        await asyncio.sleep(0)
        return
    connection = await connect()
    query = """INSERT INTO book(id, title, description, language, final_price, full_price, currency, min_age, rating, year, image, url, pages, is_audio) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)"""
    try:
        await connection.execute(query, book.Id, book.Title, book.Description, book.Language, book.Price.FinalPrice, book.Price.FullPrice,
            book.Price.Currency, book.MinAge, book.Rating, book.Year, book.Image, book.Url, book.Pages, book.IsAudio)
        logging.info(f"Успешно сохранили книгу: {book.Title}")
    except BaseException as err:
        logging.error(f"Ошибка-postgres: {err}")
    finally:
        await connection.close()
        

async def check_book_exist(book_id: int) -> bool:
    connection = await connect()
    # cursor = await connection.cursor()
    query = f"SELECT id FROM book WHERE id={book_id}"
    # await connection.execute(query)
    exists = await connection.fetchrow(query)
    await connection.close()
    
    if exists:
        logging.info(f"Книга {book_id} существует.")
        return True
    return False       

