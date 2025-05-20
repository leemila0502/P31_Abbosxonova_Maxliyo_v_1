from aiogram.types import CallbackQuery
from multi_language_bot.App import dp

@dp.callback_query()
async def uz_callback_handler(call: CallbackQuery):
    if call.data == 'uz':
        await call.message.answer(text=f"🇺🇿 O'zbek tilni tanladingiz!")
    elif call.data == 'ru':
        await call.message.answer(text=f"🇷🇺 Вы выбрали русский!")
    elif call.data == 'en':
        await call.message.answer(text=f"🇺🇸 You choose English language")