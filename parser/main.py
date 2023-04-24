import asyncio
import redis

import logging
from time import perf_counter

import api
import database
from config import RedisConfig, POOLS_COUNT, init_logs


async def main():
    red = redis.Redis(RedisConfig.Host, RedisConfig.Port)
    book_ids = (red.spop(RedisConfig.BookIdsSet) for _ in range(POOLS_COUNT))
    while book_ids:
        await scrape_couple_books(book_ids)   
        book_ids = (red.spop(RedisConfig.BookIdsSet) for _ in range(POOLS_COUNT))
    
async def scrape_couple_books(book_ids: list[str]) -> int:
    tasks = [asyncio.create_task(scrape_book(int(id.decode("utf-8")))) 
            for id in book_ids if id]
    await asyncio.gather(*tasks)
    
async def scrape_book(book_id: int):
    if await database.check_book_exist(book_id): return
    logging.info(f"Парсим книгу {book_id}")
    
    info = await api.get_book_info(book_id)
    if not info: return
    
    await database.add_book(info.Book)
    for author_id in info.IdAuthors:
        author = await api.get_author(author_id)
        await database.add_author(author, book_id)
    
    for genre_id in info.IdGenres:
        genre = await api.get_genre(genre_id)
        await database.add_genre(genre, book_id)
    

if __name__ == "__main__":
    start = perf_counter()
    init_logs()
    asyncio.run(main())
    
    print(perf_counter() - start)