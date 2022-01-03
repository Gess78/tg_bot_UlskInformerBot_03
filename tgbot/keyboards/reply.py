from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌡️ Погода"),
            KeyboardButton(text="📰 Новости")
        ],
    ],
    resize_keyboard=True,
)
