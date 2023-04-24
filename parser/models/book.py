from typing import NamedTuple

class Price(NamedTuple):
    FinalPrice: float
    FullPrice: float
    Currency: str

class Book(NamedTuple):
    Id: int
    Title: str
    Description: str
    Image: str
    IsAudio: bool
    Url: str
    Price: Price
    MinAge: int
    Language: str
    Rating: float
    Pages: int
    Year: int


class BookInfo(NamedTuple):
    Book:Book
    IdAuthors: list[id]
    IdGenres: list[id]