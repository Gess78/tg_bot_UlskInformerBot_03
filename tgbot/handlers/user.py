import math

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from telegram_bot_pagination import InlineKeyboardPaginator

import tgbot.misc.posts
from tgbot.keyboards.reply import menu


async def user_start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}!\nВыберите категорию из меню ниже",
        reply_markup=menu,
    )


ITEMS_PER_PAGE = 5


async def get_news_titles(message: Message):
    await send_posts_page(message)


async def inline_kb_answer_callback_handler(query: CallbackQuery):
    await query.message.delete()
    answer_data = query.data
    await query.answer(f"You answered with {answer_data!r}")
    page = int(query.data.split("#")[1])

    await send_posts_page(query.message, page)


async def send_posts_page(message, page=1):
    # news_titles = await get_titles()
    news_titles = tgbot.misc.posts.news_titles0

    paginator = InlineKeyboardPaginator(
        math.ceil(len(news_titles) / ITEMS_PER_PAGE),
        current_page=page,
        data_pattern="page#{page}",
    )

    text = ""
    for i in range(ITEMS_PER_PAGE):
        if (ITEMS_PER_PAGE * (page - 1) + i) < len(news_titles):
            title = news_titles[ITEMS_PER_PAGE * (page - 1) + i].get("title")
            link = news_titles[ITEMS_PER_PAGE * (page - 1) + i].get("link")
            text += f"<a href='{link}'>{title}</a>\n\n"

    await message.answer(
        text,
        reply_markup=paginator.markup,
        disable_web_page_preview=True,
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_news_titles, text=["📰 Новости"])
    dp.register_callback_query_handler(inline_kb_answer_callback_handler, text_startswith="page#")