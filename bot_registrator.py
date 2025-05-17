import asyncio
import logging
import random
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())


class FormState(StatesGroup):
    fullname = State()
    phone = State()


keyboards = [
    [
        KeyboardButton(text='Telefon 1', request_contact=True),
        KeyboardButton(text='Telefon 2', request_contact=True)
    ],
    [
        KeyboardButton(text='Telefon 3', request_contact=True)
    ],
    [
        KeyboardButton(text='Telefon 4', request_contact=True),
        KeyboardButton(text='Telefon 5', request_contact=True),
        KeyboardButton(text='Telefon 6', request_contact=True)
    ]

]

kb_markup = ReplyKeyboardMarkup(keyboard=keyboards,
                                resize_keyboard=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f'Salom. {html.bold(message.from_user.full_name)}\n\n'
        f'Ro`yxatdan o`tish uchun /register kamadasini bosing.')


@dp.message(Command('register'))
async def start_register(message: Message, state: FSMContext):
    # if not db.exists(message.chat.id):
    await state.set_state(FormState.fullname)
    return await message.reply('🧓 To`liq ismingizni kiriting: ')
    # await message.answer('Quyidagi menyulardan birini tanlang')


@dp.message(FormState.fullname)
async def get_fullname(message: Message, state: FSMContext):
    fullname = message.text
    await state.update_data(chat_id=message.chat.id, fullname=fullname)

    await message.answer('📲 Telefon raqamingizni kiriting: ', reply_markup=kb_markup)
    await state.set_state(FormState.phone)


@dp.message(FormState.phone)
async def get_phone(message: Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    await state.update_data(phone=phone_number)
    await message.answer('🎉 Siz ro`yxatdan muvaffaqiyatli o`tdingiz! ', reply_markup=ReplyKeyboardRemove())

    datas = await state.get_data()
    chat_id = datas.get('chat_id')
    fullname = datas.get('fullname')
    phone = datas.get('phone')
    text = (f"Ro'yxatdan o'tgan shaxs:\n\n"
            f"🔑 chat_id: {html.bold(chat_id)}\n"
            f"👨‍🦰 fullname: {html.italic(fullname)}\n"
            f"📱 phone: {html.bold(phone)}")
    await message.answer(text)
    # await db.save_user(chat_id, fullname, phone)

    await state.clear()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())