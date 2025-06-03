import asyncio
import logging
import random
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, DiceEmoji
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
ADMIN_ID = getenv("ADMINS")
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Salom. {html.bold(message.from_user.full_name)}\n\n')


@dp.message(Command('dice'))
async def send_diceemoji(message: Message, bot: Bot) -> None:
    emojies = [DiceEmoji.BASKETBALL, DiceEmoji.DICE, DiceEmoji.BOWLING, DiceEmoji.DART]
    emoji = emojies[random.randint(0, 3)]
    await bot.send_dice(chat_id=message.chat.id, emoji=emoji)


async def start_up(bot: Bot):
    for admin in ADMIN_ID:
        try:
            await bot.send_message(admin, 'Bot ishga tushdi')
        except Exception as e:
            print(f"{e}:{admin} id li user topilmadi .")


async def shut_dowm(bot: Bot):
    for admin in ADMIN_ID:
        try:
            await bot.send_message(admin, 'Bot o`chdi')
        except Exception as e:
            print(f"{e}:{admin} id li user topilmadi .")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.startup.register(bot)
    await dp.shutdown.register(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
