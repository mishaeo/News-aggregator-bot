from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from deep_translator import GoogleTranslator
from newspaper import build

import keyboards as kb
from database import create_or_update_user, get_user_profile

router = Router()

class number_of_articles(StatesGroup):
    quantity = State()

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
        "🧾 <b>/start</b> — Start interacting with the bot\n"
        "⚙️ <b>/registration</b> — Register or update your settings\n"
        "👤 <b>/profile</b> — View your current profile\n"
        "📰 <b>/news</b> — Latest news\n"
        "❓ <b>/help</b> — Show this help menu",
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
    await callback.answer()


@router.message(Command('news'))
async def handler_news(message: Message,  state: FSMContext):
    await message.answer('Please enter the number of articles to view!')

    await state.set_state(number_of_articles.quantity)

@router.message(number_of_articles.quantity, F.text.regexp(r'^\d+$'))
async def handler_news_outlet(message: Message,  state: FSMContext):

    await message.answer("🔍 /news command received, loading news...")

    telegram_id = message.from_user.id
    profile = await get_user_profile(telegram_id)

    number = int(message.text)

    translator = GoogleTranslator(source='auto', target=profile['language'])

    news_url = ''

    if "error" in profile:
        await message.answer(profile["error"])
    else:
        if profile['country'] == 'ru':
            if profile['category'] == 'politics':
                news_url = build('https://ria.ru/politics/', memoize_articles=False)
            elif profile['category'] == 'economics':
                news_url = build('https://www.rbc.ru/economics/', memoize_articles=False)
            elif profile['category'] == 'technology':
                news_url = build('https://www.cnews.ru/news/top/', memoize_articles=False)
            elif profile['category'] == 'general news':
                news_url = build('https://tass.ru/', memoize_articles=False)
            else:
                await message.answer('News in this category is not available')
        elif profile['country'] == 'us':
            if profile['category'] == 'politics':
                news_url = build('https://www.cnn.com/politics', memoize_articles=False)
            elif profile['category'] == 'economics':
                news_url = build('https://www.cnbc.com/economy/', memoize_articles=False)
            elif profile['category'] == 'technology':
                news_url = build('https://www.cnet.com/tech/', memoize_articles=False)
            elif profile['category'] == 'general news':
                news_url = build('https://www.nbcnews.com/news/us-news', memoize_articles=False)
            else:
                await message.answer('News in this category is not available')
        elif profile['country'] == 'de':
            if profile['category'] == 'politics':
                news_url = build('https://www.spiegel.de/politik/', memoize_articles=False)
            elif profile['category'] == 'economics':
                news_url = build('https://www.handelsblatt.com/wirtschaft/', memoize_articles=False)
            elif profile['category'] == 'technology':
                news_url = build('https://www.heise.de/news/', memoize_articles=False)
            elif profile['category'] == 'general news':
                news_url = build('https://www.dw.com/en/top-stories/s-9097', memoize_articles=False)
            else:
                await message.answer('News in this category is not available')
        else:
            await message.answer('News for this country is not available')

    await message.answer(f"Found {len(news_url.articles)} articles")

    for i, article in enumerate(news_url.articles[:number], 1):
        try:
            article.download()
            article.parse()

            translated_title = translator.translate(article.title)
            translated_text = translator.translate(article.text[:1000])

            await message.answer(f"\n{i}. {translated_title} — {article.source_url}\n")
            await message.answer(translated_text[:500] + '...')
        except Exception as e:
            await message.answer(f"{i}. Error: {e}")

