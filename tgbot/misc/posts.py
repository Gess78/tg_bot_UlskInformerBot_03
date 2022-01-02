import asyncio
import re
import timeit
import typing

import aiohttp
import aioschedule
import xmltodict
from loguru import logger

from tgbot.misc.weather import get_weather_data, get_weather_pic


@logger.catch
async def get_rss_dict(url_: str) -> typing.OrderedDict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as resp:
            if resp.status == 200:
                rss = await resp.text()
                return xmltodict.parse(rss)


async def get_tiles(rss_dict_: typing.OrderedDict):
    items = rss_dict_.get("rss").get("channel").get("item")
    res = []
    pattern = r"https://ulpressa.ru\S*?(jpg|png|jpeg)"
    for i in items:
        post_id = i.get("guid").get("#text").split("=")[1]
        title = i.get("title")
        description = i.get("description")
        short_description = description.split("/>")[-1]
        # link = i.get('link')
        link = i.get("guid").get("#text")
        if re.search(pattern, description):
            pic = re.search(pattern, description)[0]
        else:
            pic = None
        res.append(
            {
                "post_id": post_id,
                "title": title,
                "short_description": short_description,
                "link": link,
                "pic": pic,
            }
        )
    return res


news_titles0: list[dict[str, typing.Optional[str]]] = [{'': ''}]


async def get_titles():
    url = "https://ulpressa.ru/feed/"
    t00 = timeit.default_timer()
    global news_titles0
    news_titles0 = await get_tiles(await get_rss_dict(url))
    logger.info(f"ФОРМИРОВАНИЕ ЗАПИСЕЙ: {timeit.default_timer() - t00:.2f} сек.")
    # return news_titles


# a = await get_titles()


async def scheduler():
    await get_titles()
    aioschedule.every(3).minutes.do(get_titles)
    await get_weather_pic()
    aioschedule.every(3).minutes.do(get_weather_pic)
    # await get_weather_data()
    # aioschedule.every(3).minutes.do(get_weather_data)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
