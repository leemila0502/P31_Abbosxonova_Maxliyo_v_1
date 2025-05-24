import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

smiles = ['☹️ Upset', '🙂 Smile', '🤩 Happy', '😡 Angry']


class PageCallbackData(CallbackData, prefix='page'):  # 'page:next:1' yoki 'page:prev:1'
    action: str
    page: int


def page_keyboards(page: int = -1):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Avvalgi",
            callback_data=PageCallbackData(action='prev', page=page).pack()),
        InlineKeyboardButton(
            text="Keyingi",
            callback_data=PageCallbackData(action='next', page=page).pack())
    )
    return builder.as_markup()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!", reply_markup=page_keyboards())


@dp.message(Command('help', prefix='/%$'))
async def cmd_help(message: Message) -> None:
    await message.answer('Yordam')


# @dp.callback_query(PageCallbackData.filter(F.action == 'prev'))
# @dp.callback_query(PageCallbackData.filter(F.action == 'next'))
@dp.callback_query(PageCallbackData.filter())
async def callbacks_data(call: CallbackQuery, callback_data: PageCallbackData):
    page = int(callback_data.page)
    if callback_data.action == 'next':
        page += 1
        await call.message.edit_text(text=f"{smiles[page]}\n{page} - sahifa",
                                     reply_markup=page_keyboards(page))
    elif callback_data.action == 'prev':
            if page<=0:
                page=0
                await call.message.edit_text(text=f"{smiles[page]}\n{page} - sahifa",
                                             reply_markup=page_keyboards(page))
            else:
                page += -1
                await call.message.edit_text(text=f"{smiles[page]}\n{page} - sahifa",
                                         reply_markup=page_keyboards(page))



# @dp.callback_query(PageCallbackData.filter(F.action == 'prev'))
# async def callbacks_data(call: CallbackQuery, callback_data: PageCallbackData):
#     pass


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())