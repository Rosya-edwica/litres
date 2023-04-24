from database.config import connect
from database.genre import add_genre, check_genre_exist
from database.author import add_author, check_author_exist
from database.book import add_book, set_connection_between_book_and_author, set_connection_between_book_and_genre, check_book_exist