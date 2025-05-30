import asyncio
import logging
import sys
from os import getenv
import datetime

from aiogram import Bot, Dispatcher, html,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv #.env file ni o'qib olish uchun python-dotenv install qilamiz
# va (from dotenv import load_dotenv)
#shu usulda umi import qilamiz undan keyin .env ni o'qish uchun (load_dotenv()) kabi o'qib olamiz

load_dotenv()
TOKEN = getenv("BOT_TOKEN") #7032509393:AAHhTWNA-h0hCrhbdXUC1W_W4adl2edHuns token


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")
#
# @dp.message(F.text=='getMe')
# async def get_me(message: Message) -> None:
#     chat_id = message.chat.id
#     fullname = message.from_user.full_name
#     text = message.text
#     await  message.answer(f"Custom {message}!\n"
#                           f"chat_id = {chat_id}\n"
#                           f"fullname = {fullname}\n"
#                           f"text = {text}")
from datetime import datetime
@dp.message()
async def get_year(message: str) -> None:
    date_str =message
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    year = date_obj.year
    year2=datetime.today().year-year

    await  (f"sizning yoshingiz {year2} da")



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# regex need for this should write to google i hate rejex