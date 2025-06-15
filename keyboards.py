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
        InlineKeyboardButton(text="Russia", callback_data="ru"),
        InlineKeyboardButton(text="Germany", callback_data="de"),
        InlineKeyboardButton(text="USA", callback_data="us")
    ]
])

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Russian", callback_data="ru"),
        InlineKeyboardButton(text="German", callback_data="de"),
        InlineKeyboardButton(text="English", callback_data="en")
    ]
])

