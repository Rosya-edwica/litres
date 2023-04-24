import aiohttp
import asyncio

import re


async def get_json(url: str) -> dict:
    json = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status = response.status
                if status != 200: raise BaseException
                json = await response.json()
                return json["payload"]["data"]
    except BaseException:
        ...
    finally:
        await asyncio.sleep(0)
        

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