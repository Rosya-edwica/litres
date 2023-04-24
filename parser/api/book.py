from api import get_json, prepare_description, DOMAINS
from models import *


async def get_book_info(book_id: int) -> BookInfo | None:
    json = await get_json(DOMAINS.Book + str(book_id))
    if not json: return None
    info = BookInfo(
        Book=get_book(json),
        IdAuthors=[person["id"] for person in json["persons"]],
        IdGenres=[genre["id"] for genre in json["genres"]]
    )
    return info


def get_book(json: dict = None) -> Book:    
    try:
        book = Book(
        Id=json["id"],
        Title=json["title"],
        Description=prepare_description(json["html_annotation"]) if json["html_annotation"] else "",
        Image=DOMAINS.Img + json["cover_url"],
        Url=DOMAINS.Base + json["url"],
        Price=Price(
            FinalPrice=json["prices"]["final_price"],
            FullPrice=json["prices"]["full_price"],
            Currency=json["prices"]["currency"]
        ),
        MinAge=json["min_age"],
        Language=json["language_code"],
        Rating=json["rating"]["rated_avg"],
        Year=int(json["date_written_at"].split("-")[0]) if json["date_written_at"] else None,
        Pages=json["additional_info"]["current_pages_or_seconds"],
        IsAudio=False if json["art_type"] == 0 else True
        
    )
    except BaseException:
        return None
    return book
    