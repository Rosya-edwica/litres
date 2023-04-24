import asyncio

from models import Genre
from api import get_json
from config import DOMAINS

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


async def get_genre(genre_id: int) -> Genre | None:
    try:
        json = await get_json(f"{DOMAINS.Genre}/{genre_id}")
        return Genre(
        Id=json[0]["id"],
        Title=json[0]["name"],
        ParentId=None,
        Url=DOMAINS.Base + json[0]["url"],
        BooksCount=json[0]["arts_count"]
    )
    except RuntimeWarning as err:
        print(f"ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR{err}, {genre_id}")
        await asyncio.sleep(0)
        return None
    finally:
        await asyncio.sleep(0)