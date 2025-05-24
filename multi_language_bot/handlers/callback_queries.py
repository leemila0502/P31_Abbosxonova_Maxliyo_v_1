from mailbox import Message

from aiogram.types import CallbackQuery
# from multi_language_bot.App import dp
from aiogram import F, Router
from multi_language_bot.utils.db.postgres_db import PsqlDB
call_router=Router()
db=PsqlDB()
@call_router.callback_query(F.data.in_({'uz','ru','en'}))
async def uz_callback_handler(call: CallbackQuery):
    if call.data == 'uz':
        db.db_save(call.from_user.id, "uz")
        await call.message.answer(text=f"🇺🇿 O'zbek tilni tanladingiz!")
        await call.message.answer(text=f"Testni boshlash uchun /play ni bosing")
    elif call.data == 'ru':
        db.db_save(call.from_user.id, "ru")
        await call.message.answer(text=f"🇷🇺 Вы выбрали русский!")
        await call.message.answer(text=f" Чтобы начать тест нажмите /play. ")
    elif call.data == 'en':
        db.db_save(call.from_user.id, "en")
        await call.message.answer(text=f" You choose English language")
        await call.message.answer(text=f" For starting test touch to /play. ")
@call_router.callback_query(F.text=="play")
async def


