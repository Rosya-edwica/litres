from typing import NamedTuple


class Genre(NamedTuple):
    Id: int
    ParentId: int
    Title: str
    Url: str
    BooksCount: int