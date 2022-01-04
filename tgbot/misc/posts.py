import re
import timeit
import typing

import aiohttp
import xmltodict
from loguru import logger


@logger.catch
async def get_rss_dict(url_: str) -> typing.OrderedDict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as resp:
            if resp.status == 200:
                rss = await resp.text()
                return xmltodict.parse(rss)


async def get_titles():
    url = "https://ulpressa.ru/feed/"
    t00 = timeit.default_timer()
    rss_dict_ = await get_rss_dict(url)
    items = rss_dict_.get("rss").get("channel").get("item")
    posts = []
    pattern = r"https://ulpressa.ru\S*?(jpg|png|jpeg)"
    for i in items:
        post_id = i.get("guid").get("#text").split("=")[1]
        title = i.get("title")
        description = i.get("description")
        short_description = description.split("/>")[-1]
        link = i.get("guid").get("#text")
        if re.search(pattern, description):
            pic = re.search(pattern, description)[0]
        else:
            pic = None
        posts.append(
            {
                "post_id": post_id,
                "title": title,
                "short_description": short_description,
                "link": link,
                "pic": pic,
            }
        )
    logger.info(f"ФОРМИРОВАНИЕ ЗАПИСЕЙ: {timeit.default_timer() - t00:.2f} сек.")
    return posts

