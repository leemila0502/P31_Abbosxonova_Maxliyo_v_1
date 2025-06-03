import json

from aiogram import html, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from multi_language_bot.App import BASE_DIR
from multi_language_bot.keyboards.default import make_keyboards
from multi_language_bot.keyboards.inline import make_lang
from multi_language_bot.utils.db.postgres_db import pg
from multi_language_bot.utils.helper.translator import google_translate

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
    #                      f"Tilni tanlang: ",
    #                      reply_markup=three_languages())
    datas = google_translate(message.chat.id)
    await message.answer(datas['start'], reply_markup=make_keyboards([datas['change_lang_btn']]))


@start_router.message(Command('help'))
async def help_me(message: Message):
    datas = google_translate(message.chat.id)
    await message.answer(datas['help'])


@start_router.message(F.text.in_({'Изменить язык', 'Tilni o`zgartirish', 'Change language'}))
@start_router.message(Command('set_lang'))
async def set_lang(message: Message):
    datas = google_translate(message.chat.id)
    await message.answer(datas['set_lang'], reply_markup=make_lang())


@start_router.message
async def subcategory(message: Message,chat_id: int):
    lang = pg.get_lang(chat_id)
    with open(f'{BASE_DIR}/locals/{lang}/data.json', 'rb') as file:
        datas = json.load(file)
    return datas
    await message.answer(" Qaysi fandan test yechamiz ?", reply_markup=InlineKeyboardMarkup(datas["category"]))
