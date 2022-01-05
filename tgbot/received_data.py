import asyncio
import typing
from dataclasses import dataclass

from loguru import logger

from tgbot.misc.posts import get_posts
from tgbot.misc.weather import get_weather_data


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Data:
    weather: dict
    posts: list[dict[str, typing.Optional[str]]]
    misc: typing.Optional[dict] = None


async def load_data() -> Data:
    return Data(
        weather=await get_weather_data(),
        posts=await get_posts(),
    )


async def update_data():
    data.weather = await get_weather_data()
    data.posts = await get_posts()


loop = asyncio.get_event_loop()
data: Data = loop.run_until_complete(load_data())  # Будет ждать, пока some_function не закончит выполнение.
logger.info('Initial loading done...')
