import requests
import asyncio
from functools import partial

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


import keyboards as kb
from database import create_or_update_user, get_user_profile
from config import API_KEY, URL

router = Router()

class RegistrationState(StatesGroup):
    telegram_id = State()
    category = State()
    country = State()
    language = State()

@router.message(CommandStart())
async def handler_start(message: Message):
    await message.answer('👋 Welcome to the News aggregator bot!\n Type /help to find out what this bot can do.')

@router.message(Command("profile"))
async def handler_profile(message: Message):
    telegram_id = message.from_user.id
    profile = await get_user_profile(telegram_id)

    if "error" in profile:
        await message.answer(profile["error"])
    else:
        await message.answer(
            f"📋 Your Profile:\n"
            f"🌍 Country: {profile['country']}\n"
            f"📂 Category: {profile['category']}\n"
            f"🗣 Language: {profile['language']}"
        )

@router.message(Command("help"))
async def handler_help(message: Message):
    await message.answer(
        "ℹ️ <b>Help Menu</b>\n\n"
        "🧾 <b>/start</b> — Начать работу с ботом\n"
        "⚙️ <b>/registration</b> — Пройти регистрацию или изменить настройки\n"
        "👤 <b>/profile</b> — Посмотреть ваш текущий профиль\n"
        "📰 <b>/news</b> — Последние новости\n"
        "❓ <b>/help</b> — Показать это меню помощи",
        parse_mode="HTML"
    )

@router.message(Command("registration"))
async def handler_select_of_id(message: Message,  state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(telegram_id=user_id)

    await message.answer('Select the news category you are interested in.', reply_markup=kb.category_button)
    await state.set_state(RegistrationState.category)

@router.message(RegistrationState.category, F.text.in_(['politics', 'economics', 'technology', 'general news']))
async def handler_select_of_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)

    await message.answer('Great! Now enter your country.', reply_markup=kb.country_keyboard)
    await state.set_state(RegistrationState.country)

@router.callback_query(RegistrationState.country, lambda c: c.data in ['ru', 'de', 'us'])
async def handler_select_country_callback(callback: CallbackQuery, state: FSMContext):
    country = callback.data
    await state.update_data(country=country)

    await callback.message.answer("Great! Now enter your language.", reply_markup=kb.language_keyboard)
    await state.set_state(RegistrationState.language)

    await callback.answer()

@router.callback_query(RegistrationState.language, lambda c: c.data in ['ru', 'de', 'en'])
async def handler_select_of_language(callback: CallbackQuery, state: FSMContext):
    language = callback.data
    await state.update_data(language=language)

    data = await state.get_data()
    telegram_id = data.get('telegram_id')
    category = data.get('category')
    country = data.get('country')
    language = data.get('language')

    await create_or_update_user(
        telegram_id=telegram_id,
        category=category,
        country=country,
        language=language
    )

    await state.clear()