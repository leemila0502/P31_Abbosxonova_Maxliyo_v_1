
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

async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\n")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = (f"b yoki strong : <b>Aiogram</b>\n"
            f"i yoki em : <i>Aiogram</i>\n"
            f"u yoki ins : <u>Aiogram</u>\n"
            f"s,strick yoki del : <del>Aiogram</del>\n"
            f"span yoki tg_spoiler : <span class='tg-spoiler'>Aiogram</span>\n"
            f"rasm <a href=\"https://www.google.com/imgres?q=nature%27&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fc%2Fc8%2FAltja_j%25C3%25B5gi_Lahemaal.jpg&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FNature_photography&docid=oxi7l2kbi9T7QM&tbnid=3mkrlRZIBbznCM&vet=12ahUKEwjxosXMpKWNAxVLnP0HHT35DHAQM3oECBcQAA..i&w=4390&h=2948&hcb=2&ved=2ahUKEwjxosXMpKWNAxVLnP0HHT35DHAQM3oECBcQAA\">inline URL</a>")

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\n"+text)




@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

