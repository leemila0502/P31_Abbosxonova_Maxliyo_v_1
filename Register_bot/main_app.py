import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from Register_bot.ORM import init_db

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
ADMINS = getenv('ADMIN').split(',')
dp = Dispatcher()


def main_menu(is_admin=False):
    if is_admin:
        buttons = [
            [InlineKeyboardButton(text="➕Foydalanuvchi qo'shish➕", callback_data='add_user')],
            [InlineKeyboardButton(text="👀Barcha foydalanuvchilarni ko'rish👀", callback_data='view_users')],
            [InlineKeyboardButton(text="⛔Foydalanuvchini o'chirish⛔", callback_data='delete_user')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        buttons = [[InlineKeyboardButton(text="👀Ma'lumotimni ko'rish👀", callback_data='view_me')],
                   [InlineKeyboardButton(text="🆕Ma'lumotimni yangilash🆕", callback_data='update_me')],
                   [InlineKeyboardButton(text="⛔Ma'lumotimni o'chirish⛔", callback_data='delete_me')]
                   ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)


def update():
    buttons = [
        [InlineKeyboardButton(text="💬Email", callback_data='email')],
        [InlineKeyboardButton(text="📱Phone", callback_data='phone')],
        [InlineKeyboardButton(text="📃Address", callback_data='address')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def on_startup():
    await init_db()


async def main() -> None:
    from Register_bot.handlers import callback_router
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(on_startup)
    dp.include_router(callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



