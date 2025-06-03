import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
ADMINS = getenv('ADMINS').split(',')
dp = Dispatcher()


async def main() -> None:
    from inline_bot_with_api.handlers import start_router,wiki_router
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router,   wiki_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())