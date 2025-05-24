import asyncio
import logging
import sys
from os import getenv
from random import random

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv  # .env file ni o'qib olish uchun python-dotenv install qilamiz

# va (from dotenv import load_dotenv)
# shu usulda umi import qilamiz undan keyin .env ni o'qish uchun (load_dotenv()) kabi o'qib olamiz

load_dotenv()
TOKEN = getenv("BOT_TOKEN")  # 7032509393:AAHhTWNA-h0hCrhbdXUC1W_W4adl2edHuns token

dp = Dispatcher(storage=MemoryStorage())

class GameState(StatesGroup):
    guessing=State()

    @dp.message(CommandStart())
    async def command_start(self, message: Message):
        guess_num=random.randint(1,100)
        await state.set_state(GameState.guessing)
        await state.update_state(guess_num=guess_num,attemp=0)
        await message.answer('Men 1 va 100 oraligidagi son o`yladim . toping!')
    #
    # @dp.message()
    # async def echo_handler(message: Message) -> None:
    #         await message.send_copy(chat_id=message.chat.id)


@dp.message(GameState.guessing)
async def loop_state(message: Message,state:FSMContext) -> None:
        text=message.text
        await message.answer(f"six {html.bold(text)}")






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

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\n" + text)


@dp.message(F.photo)
async def command_photo_handler(message: Message) -> None:
    await message.answer('you send photo !')


@dp.message(F.document)
async def command_doc_handler(message: Message) -> None:
    await message.answer('you send document !')


@dp.message(F.sticker)
async def command_emoji_handler(message: Message) -> None:
    await message.answer('you send sticker !')


@dp.message(F.location)
async def command_loc_handler(message: Message) -> None:
    lat=message.location.latitude
    lon=message.location.longitude

    await message.answer('you send location !\n'+f"{lat}\n"+ f"{lon}")



@dp.message(F.text=='Asal qzmana qara')
async def asallikka_tekshirish(message: Message) -> None:

    await message.answer("Shunaqa asalligizdan Arila hijolat 😘")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

