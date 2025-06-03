import json
from aiogram.types import Message, InlineKeyboardMarkup

from aiogram.types import CallbackQuery
# from multi_language_bot.App import dp
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from multi_language_bot.handlers.Callbacks import CategoryCallback, SubCategoryCallback, BackCallback, Level

from multi_language_bot.utils.db.postgres_db import PsqlDB, pg
from multi_language_bot.App import BASE_DIR

call_router = Router()
from multi_language_bot.utils.helper.functions_json import Functions

db = PsqlDB()


@call_router.callback_query(F.data.in_({'uz', 'ru', 'en'}))
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


func = Functions()


@call_router.message(F.text == "/play")
async def choose_subc(message: Message):
    chatid = message.chat.id
    lang = pg.get_lang(chatid)

    category = func.categories(lang)
    builder = InlineKeyboardBuilder()
    for cat_id, name in category:
        builder.button(text=name, callback_data=CategoryCallback(id=cat_id))
    builder.adjust(2)
    await message.answer("Bo'limni tanlang:", reply_markup=builder.as_markup())


@call_router.callback_query(CategoryCallback.filter())
async def choose_cat(call: CallbackQuery, callback_data: CategoryCallback):
    lg=pg.get_lang(call.from_user.id)
    sub = func.subcategories(lg)
    builder = InlineKeyboardBuilder()
    x=callback_data.id
    for item in sub:
        if item[1] == x:

           builder.button(
               text=item[2],
               callback_data=SubCategoryCallback(id=item[0], category=callback_data.id)
               )

    builder.button(
    text="⬅️ Ortga",
    callback_data=BackCallback(level=Level.CATEGORY.value))

    builder.adjust(2)
    await call.message.edit_text("Bo'lim darajalari:", reply_markup=builder.as_markup())

@call_router.callback_query(SubCategoryCallback.filter())
async def agreement(call: CallbackQuery, callback_data: SubCategoryCallback):
    lg=pg.get_lang(call.from_user.id)
    category_name=func.categoriesa(lg,callback_data.id)
    subcategory_name=func.subcategoriesa(lg,sub_id=callback_data.id,catid=callback_data.category)
    data=func.get_quizzes(category_name,subcategory_name,lg)
    builder = InlineKeyboardBuilder()







