from typing import Dict
import aiosqlite

DB_NAME = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id BIGINT UNIQUE NOT NULL,
                country VARCHAR(5) NOT NULL,
                category VARCHAR(20) NOT NULL,
                language TEXT DEFAULT 'en'
            )
        """)
        await db.commit()

async def create_or_update_user(telegram_id: int, category: str, country: str, language: str = 'en'):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, category, country, language)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                category=excluded.category,
                country=excluded.country,
                language=excluded.language
        """, (telegram_id, category, country, language))
        await db.commit()

async def get_user_by_id(telegram_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return await cursor.fetchone()

async def get_user_profile(telegram_id: int) -> Dict[str, str]:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT country, category, language FROM users WHERE telegram_id = ?", (telegram_id,)
        )
        row = await cursor.fetchone()

    if row:
        country, category, language = row
        return {
            "country": country,
            "category": category,
            "language": language
        }
    else:
        return {
            "error": "⚠️ You are not registered yet. Use /registration to register."
        }



