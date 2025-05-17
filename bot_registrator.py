import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from dotenv import load_dotenv
from datetime import datetime
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
import psycopg2


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
PASSWORD =  getenv("a33333")
conn = psycopg2.connect(user = 'postgres', host = 'localhost', password = PASSWORD, port = 5432, database = 'tg_users')
cursor = conn.cursor()

dp = Dispatcher()


class Reg(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    email = State()




class DATABASE():
    @staticmethod
    def save(chat_id, first_name, last_name, age, email):
        cursor.execute(
            "INSERT INTO tg_users (chat_id, first_name, last_name, age, email) VALUES (%s, %s, %s, %s, %s)",
            (chat_id, first_name, last_name, age, email)
        )
        conn.commit()

    @staticmethod
    def is_registered(chat_id):
        cursor.execute("SELECT 1 FROM tg_users WHERE chat_id=%s", (chat_id,))
        return cursor.fetchone() is not None



@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    if DATABASE.is_registered(message.chat.id):
        await message.answer("Ты уже зарегестрирован! ")
        return
    await message.answer("Привет,можешь пожалуйста ввести свое имя?")
    await state.set_state(Reg.first_name)


@dp.message(Reg.first_name)
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text.capitalize())

    await message.answer("напиши свою фамилию")
    await state.set_state(Reg.last_name)


@dp.message(Reg.last_name)
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text.capitalize())

    await message.answer("напиши свой возраст")
    await state.set_state(Reg.age)


@dp.message(Reg.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer("напиши свой эмеил")
    await state.set_state(Reg.email)


@dp.message(Reg.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()

    @dp.message(Command("followers"))
    async def get_followers(message: Message):
        cursor.execute("SELECT COUNT(*) FROM tg_users")
        count = cursor.fetchone()[0]
        await message.answer(f"Всего пользователей: {count}")


    DATABASE.save(
        chat_id=message.chat.id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=int(data["age"]),
        email=data["email"]
    )

    await message.answer("Регистрация завершена ✅")
    await state.clear()