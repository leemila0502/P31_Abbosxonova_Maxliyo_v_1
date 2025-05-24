# from multi_language_bot.App import dp
from aiogram import html,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from multi_language_bot.keyboards.inline import make_lang
from multi_language_bot.utils.helper.translator import google_translate
start_router=Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Tilni tanlang: ",
                         reply_markup=make_lang())
    # datas = google_translate(message.chat.id)
    # await message.answer(datas['start'])


@start_router.message(CommandStart(Command("help")))
async def help_me(message: Message) -> None:
    datas=google_translate(message.chat_id)
    await message.answer(datas['help'])




