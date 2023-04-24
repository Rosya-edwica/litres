from typing import NamedTuple


class Author(NamedTuple):
    Id: int
    FullName: str
    Description: str
    Image: str
    Url: str
    BooksCount: int