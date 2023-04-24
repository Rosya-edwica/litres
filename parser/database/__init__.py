from database.config import connect
from database.genre import add_genre, check_genre_exist, set_connection_between_book_and_genre
from database.author import add_author, check_author_exist, set_connection_between_book_and_author
from database.book import add_book, check_book_exist