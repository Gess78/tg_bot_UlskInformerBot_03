import math

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InputFile
from loguru import logger
from telegram_bot_pagination import InlineKeyboardPaginator

import tgbot.misc.posts
from tgbot.keyboards.reply import menu

from tgbot.config import config
from tgbot.received_data import data


async def user_start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}!\nВыберите категорию из меню ниже",
        reply_markup=menu,
    )


async def get_news_titles(message: Message):
    await send_posts_page(message)


async def inline_kb_answer_callback_handler(query: CallbackQuery):
    await query.message.delete()
    answer_data = query.data
    await query.answer(f"You answered with {answer_data!r}")
    page = int(query.data.split("#")[1])

    await send_posts_page(query.message, page)


async def send_posts_page(message, page=1):
    items_per_page = config.misc.items_per_page
    news_titles = tgbot.received_data.data.posts.data

    paginator = InlineKeyboardPaginator(
        math.ceil(len(news_titles) / items_per_page),
        current_page=page,
        data_pattern="page#{page}",
    )

    text = ""
    for i in range(items_per_page):
        if (items_per_page * (page - 1) + i) < len(news_titles):
            title = news_titles[items_per_page * (page - 1) + i].get("title")
            link = news_titles[items_per_page * (page - 1) + i].get("link")
            text += f"<a href='{link}'>{title}</a>\n\n"

    await message.answer(
        text,
        reply_markup=paginator.markup,
        disable_web_page_preview=True,
    )


# @logger.catch
# async def send_weather(message: Message):
#     weather_data = data.weather
#     text = [
#         "Погода:",
#         f"{weather_data.icon}",
#         f"{weather_data.description.capitalize()}, {weather_data.temp}°",
#         f"Ощущается как: {weather_data.temp_feels_like}°",
#         f"Давление: {weather_data.pressure} мм рт.ст.",
#         f"Влажность: {weather_data.humidity}%",
#         f"Ветер: {weather_data.wind_speed} м/с, {weather_data.wind_direction}",
#     ]
#
#     await message.answer("\n".join(text))


@logger.catch
async def send_weather_pic(message: Message):
    weather_data = data.weather
    text = [
        # "Погода:",
        f"{weather_data.dt}",
        f"{weather_data.description.capitalize()}",
        f"Температура: {weather_data.temp}°",
        f"ощущается как: {weather_data.temp_feels_like}°",
        f"Давление: {weather_data.pressure} мм рт.ст.",
        f"Влажность: {weather_data.humidity}%",
        f"Ветер: {weather_data.wind_speed} м/с, {weather_data.wind_direction}",
    ]
    await message.answer_document(document=InputFile(path_or_bytesio=f"tgbot/media/images/{weather_data.icon}.webp"),
                                  caption="\n".join(text))
    await message.answer("\n".join(text))


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_news_titles, text=["📰 Новости"])
    # dp.register_message_handler(send_weather, text=["🌡️ Погода"])
    dp.register_message_handler(send_weather_pic, text=["🌡️ Погода"])
    dp.register_callback_query_handler(inline_kb_answer_callback_handler, text_startswith="page#")
