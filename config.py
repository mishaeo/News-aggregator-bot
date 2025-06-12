from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_KEY = os.getenv("NEWSAPI_KEY")

URL = os.getenv("URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")