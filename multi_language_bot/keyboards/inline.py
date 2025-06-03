from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_lang():
    kbs = [
        [
            InlineKeyboardButton(text='🇺🇿 uz', callback_data='uz'),
            InlineKeyboardButton(text='🇷🇺 ru', callback_data='ru'),
            InlineKeyboardButton(text='🇺🇸 en', callback_data='en'),
            InlineKeyboardButton(text='Instagram', url='https://instagram.com'),

        ]
    ]
    uz_ru_en_kbs = InlineKeyboardMarkup(inline_keyboard=kbs)
    return uz_ru_en_kbs


def make_category(group):

   button=[]
   for data in group[1]:
       button=InlineKeyboardButton(text=data['text'], callback_data=data['callback_data'])

