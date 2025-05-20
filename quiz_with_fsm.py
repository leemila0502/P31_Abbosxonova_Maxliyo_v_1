import asyncio
import logging
import sys
from collections import defaultdict
from os import getenv
from sre_parse import State

import psycopg2
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())


class States:
    category = State()
    asking_question = State()
    result = State()


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='quiz_dbb',
            user='postgres',
            password='a33333',
            host='localhost',
            port='5432'
        )
        self.curr = self.conn.cursor()

    def execute(self, query):
        with self.conn:
            self.curr.execute(query)
        return self.curr

    def questions(self):
        query = f"""select quiz.question,option.option_text,option.is_correct from quiz join option on quiz.id=option.quiz_id;"""
        curr = self.execute(query)
        return curr.fetchall()

    def taking_questions(self):
        rows = self.questions()
        questions_dict = defaultdict(lambda: {"options": [], "correct_answer": None})

        for question, option, is_correct in rows:
            questions_dict[question]["options"].append(option)
            if is_correct == 1:
                questions_dict[question]["correct_answer"] = option

        # Yakuniy ro‘yxatga aylantiramiz
        result = []
        for question, data in questions_dict.items():
            result.append({
                "question": question,
                "options": data["options"],
                "correct_answer": data["correct_answer"]
            })

        return result


@dp.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Kategoriyani kiriting", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Matematika"), KeyboardButton(text='Fizika')]], resize_keyboard=True))
    await state.set_state(States.category)


@dp.message(States.category)
async def question_handler(message: Message, state: FSMContext):
    categorys = message.text
    await state.update_data(categorys)
    questions = Database().taking_questions()
    await state.update_data(questions=questions, current_q=0, correct=0)
    await send_question(message, state)


@dp.message
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
