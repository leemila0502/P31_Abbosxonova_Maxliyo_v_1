import asyncio
import logging
import sys
from dataclasses import dataclass
from os import getenv, path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
TG_TOKEN = getenv('TG_TOKEN')
API_TOKEN = getenv('API_TOKEN')

dp = Dispatcher()

BASE_DIR = path.dirname(path.abspath(__file__))
print(BASE_DIR)

@dataclass
class QuizState(StatesGroup):
    confirm: State()
    play:State()


@dataclass
class Questions:
    subcategory:str
    category: str
    text:str
    options: list[str]
    correct_answer:str

import json



async def main() -> None:
    from multi_language_bot.handlers import start_router, call_router

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router, call_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())