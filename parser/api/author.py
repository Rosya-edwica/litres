from api import get_json, prepare_description
from config import DOMAINS
from models import Author
import logging

async def get_author(author_id: int) -> Author | None:
    json = await get_json(DOMAINS.Author + str(author_id))
    if not json: return
    try:
        author = Author(
        Id=author_id,
        FullName=json["full_name"],
        Description=prepare_description(json["about_author"]) if json["about_author"] else "",
        Image=DOMAINS.Img + json["image_url"] if json["image_url"] else None,
        Url=DOMAINS.Base + json["url"],
        BooksCount=json["arts_count"]
        )
    except BaseException as err:
        logging.error(f"Ошибка при парсинге автора: {author_id} - {err}")
        return
    return author

