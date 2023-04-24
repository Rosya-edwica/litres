import re
from typing import NamedTuple
import aiohttp
import asyncio

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

async def get_json(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status = response.status
            if status != 200: 
                await asyncio.sleep(0)
                return 
            json = await response.json()
            return json["payload"]["data"]


async def get_payload(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            status = response.status
            if status != 200: return
            json = await response.json()
            return json["payload"]


def prepare_description(text: str) -> str:
    """Форматируем текст для вывода в HTMl-формате"""
    text = re.sub(r"\[", "<", text)
    text = re.sub(r"\]", ">", text)
    text = re.sub(r"\n", "<br/>", text)
    text = re.sub(r"\r", "", text)
    return text