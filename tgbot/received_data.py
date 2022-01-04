import asyncio
import typing
from dataclasses import dataclass

from loguru import logger

from tgbot.misc.posts import get_titles
from tgbot.misc.weather import get_weather_data


@dataclass
class Weather:
    dt: int
    icon: str
    description: str
    temp: int
    temp_feels_like: int
    pressure: int
    humidity: int
    wind_speed: int
    wind_direction: str


@dataclass
class Posts:
    data: list[dict[str, typing.Optional[str]]]


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Data:
    weather: Weather
    posts: Posts
    misc: Miscellaneous


async def load_data() -> Data:
    weather_data = await get_weather_data()
    posts_data = await get_titles()

    return Data(
        weather=Weather(
            dt=weather_data["dt"],
            icon=weather_data["icon"],
            description=weather_data["description"],
            temp=weather_data["temp"],
            temp_feels_like=weather_data["temp_feels_like"],
            pressure=weather_data["pressure"],
            humidity=weather_data["humidity"],
            wind_speed=weather_data["wind_speed"],
            wind_direction=weather_data["wind_direction"],
        ),
        posts=Posts(data=posts_data),
        misc=Miscellaneous(),
    )


loop = asyncio.get_event_loop()
data: Data = loop.run_until_complete(load_data())  # Будет ждать, пока some_function не закончит выполнение.
logger.info('Initial loading done...')
