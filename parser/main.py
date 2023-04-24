import logging
from time import perf_counter

import database
import api
import asyncio
import redis


logging.basicConfig(filename="logs.info", filemode='w', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
print("logs.info")


SET_UNPARSED_BOOKS = "not_parsed"


async def main():
    red = redis.Redis(host="127.0.0.1", port=6379)
    book_ids = (red.spop(SET_UNPARSED_BOOKS) for _ in range(50))
    while book_ids:
        await scrape_couple_books(book_ids)   
        book_ids = (red.spop(SET_UNPARSED_BOOKS) for _ in range(50))

async def scrape_couple_books(book_ids: list[str]) -> int:
    tasks = [asyncio.create_task(scrape_book(int(id.decode("utf-8")))) 
            for id in book_ids if id]
    await asyncio.gather(*tasks)
    
async def scrape_book(book_id: int):
    if database.check_book_exist(book_id): return
    logging.info(f"Парсим книгу {book_id}")
    
    info = await api.get_book_info(book_id)
    if not info: return
    database.add_book(info.Book)
    
    for author_id in info.IdAuthors:
        if not database.check_author_exist(author_id):
            author = await api.get_author(author_id)
            database.add_author(author)
        database.set_connection_between_book_and_author(info.Book.Id, author_id)
    
    for genre_id in info.IdGenres:
        if not database.check_genre_exist(genre_id):
            genre = await api.get_genre(genre_id)
            database.add_genre(genre)
        database.set_connection_between_book_and_genre(info.Book.Id, genre_id)
        

if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(main())
    print(perf_counter() - start)