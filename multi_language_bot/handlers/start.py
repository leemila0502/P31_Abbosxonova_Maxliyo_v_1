from multi_language_bot.App import dp
from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message
from multi_language_bot.keyboards.inline import make_lang

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Tilni tanlang: ",
                         reply_markup=make_lang())
