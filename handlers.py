from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import keyboards as kb
from database import create_or_update_user, get_user_profile

router = Router()

class RegistrationState(StatesGroup):
    telegram_id = State()
    category = State()
    country = State()
    language = State()

@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer('👋 Welcome to the News aggregator bot!\n Type /help to find out what this bot can do.')

@router.message(Command("registration"))
async def command_select_of_id(message: Message,  state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(telegram_id=user_id)

    await message.answer('Select the search category you are interested in', reply_markup=kb.category_button)
    await state.set_state(RegistrationState.category)

@router.message(RegistrationState.category, F.text.in_(['Politics', 'Economics', 'Social media']))
async def command_select_of_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)

    await message.answer('Great! Now enter your country:')
    await state.set_state(RegistrationState.country)

@router.message(RegistrationState.country)
async def command_select_of_country(message: Message, state: FSMContext):
    country = message.text
    await state.update_data(country=country)

    await message.answer('Great! Now enter your language:')
    await state.set_state(RegistrationState.language)

@router.message(RegistrationState.language)
async def command_select_of_language(message: Message, state: FSMContext):
    language = message.text
    await state.update_data(language=language)

    data = await state.get_data()
    telegram_id = data.get('telegram_id')
    category = data.get('category')
    country = data.get('country')

    await create_or_update_user(
        telegram_id=telegram_id,
        category=category,
        country=country,
        language=language
    )

    await state.clear()

@router.message(Command("profile"))
async def profile_handler(message: Message):
    telegram_id = message.from_user.id
    profile_text = await get_user_profile(telegram_id)
    await message.answer(profile_text)

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "ℹ️ <b>Help Menu</b>\n\n"
        "🧾 <b>/start</b> — Начать работу с ботом\n"
        "⚙️ <b>/registration</b> — Пройти регистрацию или изменить настройки\n"
        "👤 <b>/profile</b> — Посмотреть ваш текущий профиль\n"
        "❓ <b>/help</b> — Показать это меню помощи",
        parse_mode="HTML"
    )




