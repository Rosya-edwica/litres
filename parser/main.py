import logging
from time import perf_counter

import database
import api
import asyncio

logging.basicConfig(filename="logs.info", filemode='w', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
print("logs.info")


async def main():
    next_page = await scrape_page()
    count = 1
    while next_page:
        print(f"Page: {count}")
        count += 1
        next_page = await scrape_page(page_token=next_page)

async def scrape_page(page_token: str = None) -> str | None:
    url = "https://api.litres.ru/foundation/api/arts"
    if page_token: url = "https://api.litres.ru/foundation" + page_token
    logging.info(f"Парсим страницу: {url}")    

    json = await api.get_payload(url)
    id_books = [item["id"] for item in json["data"]]
    tasks = [asyncio.create_task(scrape_book(id_book)) for id_book in id_books]
    await asyncio.gather(*tasks)
    
    return json["pagination"]["next_page"]

async def scrape_book(book_id: int):
    if database.check_book_exist(book_id): return
    logging.info(f"Парсим книгу {book_id}")
    info = await api.get_book_info(book_id)
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
    