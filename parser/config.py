import yaml
import logging
from typing import NamedTuple

class __RedisConfig(NamedTuple):
    Host: str
    Port: int
    BookIdsSet: str


class __PostgresConfig(NamedTuple):
    Host: str
    Port: int
    User: str
    Pass: str
    Database: str

class __Domains(NamedTuple):
    Base: str
    Img: str
    Author: str
    Book: str
    Genre: str
    

DOMAINS = __Domains(
    Base="https://www.litres.ru",
    Img="https://cv9.litres.ru",
    Author="https://api.litres.ru/foundation/api/authors/",
    Book="https://api.litres.ru/foundation/api/arts/",
    Genre="https://api.litres.ru/foundation/api/genres"
)

with open("config.yml", "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)


POOLS_COUNT = int(yaml_data["polls"])    

RedisConfig = __RedisConfig(
    Host=yaml_data["redis"]["host"],
    Port=int(yaml_data["redis"]["port"]),
    BookIdsSet=yaml_data["redis"]["book_ids_set"]
)

PostgresConfig = __PostgresConfig(
    Host=yaml_data["db"]["host"],
    Port=int(yaml_data["db"]["port"]),
    User=yaml_data["db"]["user"],
    Pass=yaml_data["db"]["password"],
    Database=yaml_data["db"]["database"]
)


def init_logs():
    logging.basicConfig(filename="logs.info", filemode='w', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)