from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

category_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Politics"),
         KeyboardButton(text="Economics"),
         KeyboardButton(text="Social media")]
    ],
    resize_keyboard=True
)