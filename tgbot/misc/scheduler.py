import asyncio

import aioschedule

from tgbot.misc.posts import get_titles
from tgbot.misc.weather import get_weather_data


async def scheduler():
    aioschedule.every(1).minutes.do(get_titles)
    aioschedule.every(1).minutes.do(get_weather_data)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
