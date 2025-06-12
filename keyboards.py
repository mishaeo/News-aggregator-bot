from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

category_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="politics")],
        [KeyboardButton(text="economics")],
        [KeyboardButton(text="technology")],
        [KeyboardButton(text="general news")],
    ],
    resize_keyboard=True
)

country_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Россия", callback_data="ru"),
        InlineKeyboardButton(text="Германия", callback_data="de"),
        InlineKeyboardButton(text="США", callback_data="us")
    ]
])

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Русский", callback_data="ru"),
        InlineKeyboardButton(text="Немецкий", callback_data="de"),
        InlineKeyboardButton(text="английский", callback_data="en")
    ]
])

