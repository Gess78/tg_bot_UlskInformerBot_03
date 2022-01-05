import asyncio

import aioschedule

from tgbot.received_data import load_data, update_data
from tgbot.misc.posts import get_posts
from tgbot.misc.weather import get_weather_data


async def scheduler():
    # aioschedule.every(30).minutes.do(get_titles)
    # aioschedule.every(30).minutes.do(get_weather_data)
    # aioschedule.every(10).seconds.do(get_posts)
    # aioschedule.every(10).seconds.do(get_weather_data)
    aioschedule.every(10).seconds.do(update_data)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
