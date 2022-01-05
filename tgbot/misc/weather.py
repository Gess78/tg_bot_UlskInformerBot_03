import aiohttp
from loguru import logger

from tgbot.config import config
import datetime


def wind_deg_to_str2(deg):
    arr = [
        "северо-восточный",
        "восточный",
        "юго-восточный",
        "южный",
        "юго-западный",
        "западный",
        "северо-западный",
        "северный",
    ]
    return arr[int(abs((deg - 22.5) % 360) / 45)]


@logger.catch
async def get_weather_data():
    url_ = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "id=479123&"
        f"appid={config.misc.openweathermap_token}&"
        "lang=ru&"
        "units=metric"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as resp:
            json_data = await resp.json()
            dt = datetime.datetime.fromtimestamp(json_data.get("dt")).isoformat()
            weather_data = {
                "dt": dt,
                "icon": json_data.get("weather")[0].get("icon"),
                "description": json_data.get("weather")[0].get("description"),
                "temp": int(json_data.get("main").get("temp")),
                "temp_feels_like": int(json_data.get("main").get("feels_like")),
                "pressure": int(json_data.get("main").get("pressure") * 0.750064),
                "humidity": int(json_data.get("main").get("humidity")),
                "wind_speed": int(json_data.get("wind").get("speed")),
                "wind_direction": wind_deg_to_str2(json_data.get("wind").get("deg")),
            }
            logger.info("ПОГОДА ПОЛУЧЕНА :)")
        return weather_data
