from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import keyboards as kb

router = Router()

class RegistrationState(StatesGroup):
    telegram_id = State()
    category = State()
    country = State()

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer('👋 Welcome to the News aggregator bot!')

@router.message(Command("setting"))
async def handle_popular_selection(message: Message,  state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(telegram_id=user_id)

    await message.answer('Select the search category you are interested in', reply_markup=kb.category_button)
    await state.set_state(RegistrationState.category)

@router.message(RegistrationState.category, F.text.in_(['Politics', 'Economics', 'Social media']))
async def process_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)

    await message.answer('Great! Now enter your country:')
    await state.set_state(RegistrationState.country)

@router.message(RegistrationState.country)
async def process_country(message: Message, state: FSMContext):
    country = message.text
    await state.update_data(country=country)

    data = await state.get_data()
    await message.answer(f"Your ID: {data.get('telegram_id')}\nCategory: {data.get('category')}\nCountry: {country}")

    await state.clear()
