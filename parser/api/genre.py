from models import Genre
from api import get_json, DOMAINS
import asyncio

async def get_all_genres() -> list[Genre]:
    json = await get_json(DOMAINS.Genre)
    genres = get_subgenres(json)
    return genres

def get_subgenres(json_genre: list[dict], parent_id: int = None) -> list[Genre]:
    genres: list[Genre] = []
    for item in json_genre:
        genres.append(Genre(
            Id=item["id"],
            Title=item["name"],
            ParentId=parent_id,
            Url=DOMAINS.Base + item["url"],
            BooksCount=item["arts_count"]
        ))
        genres += get_subgenres(item["subgenres"], parent_id=item["id"])
    return genres


async def get_genre(genre_id: int) -> Genre:
    try:
        json = await get_json(f"{DOMAINS.Genre}/{genre_id}")[0]
        return Genre(
        Id=json["id"],
        Title=json["name"],
        ParentId=None,
        Url=DOMAINS.Base + json["url"],
        BooksCount=json["arts_count"]
    )
    except BaseException:
        await asyncio.sleep(0)
        return None