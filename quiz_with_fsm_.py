import asyncio
import logging
from dataclasses import dataclass
import sys
from os import getenv

import psycopg2
from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


def save_to_database(message: Message,count_true=0,count_false=0):
    conn = psycopg2.connect(
        dbname="quiz_dbb",
        user="postgres",
        password="a33333",
        host="localhost"
    )
    chat_ids=message.chat.id
    cur = conn.cursor()
    cur.execute("""create table if not exists results(chat_id integer, correct integer,incorrect integer) ;""")
    cur.execute(f"insert into results (chat_id,correct,incorrect) values ({chat_ids},{count_true},{count_false})")
    conn.commit()
    cur.close()
    conn.close()

def results_shower():
    conn = psycopg2.connect(
        dbname="quiz_dbb",
        user="postgres",
        password="a33333",
        host="localhost"
    )

    cur = conn.cursor()
    cur.execute(f"select * from results ")
    results=cur.fetchall()
    cur.close()
    conn.close()
    return results

@dataclass
class Questions:
    text:str
    options: list[str]
    correct_answer:str

questions = [
        Questions(text='2 * 4 = ?', options=['8', '9', '10', '11'], correct_answer='8'),
        Questions(text='2 - 4 = ?', options=['-2', '3', '0', '1'], correct_answer='-2'),
        Questions(text='2x * 4 = 0', options=['0', '9', '10', '11'], correct_answer='0'),
    ]


@dataclass
class QuizState(StatesGroup):
    confirm=State()
    playing=State()

def make_keyboard(options,rows):
    button=[KeyboardButton(text=o) for o in options ]
    keyboard=[button[i:i+rows] for i in range(0,len(button),rows)]
    return ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)

@dp.message(CommandStart())
async def start_handler(message:Message):
    await message.answer(f"Salom {html.bold(message.from_user.full_name)}!\n\n"
                         f"O'yinni boshlash uchun /play ni bosing.😊",
    reply_markup=ReplyKeyboardRemove())

@dp.message(Command('play'))
async def play_handler(message:Message,state:FSMContext):
    await state.set_state(QuizState.confirm)
    await message.answer(f"Savollar soni {len(questions)} ta, o'ynaymizmi ?\n\n",
                         reply_markup=make_keyboard(['Ha','Yo`q'],rows=2))


@dp.message(QuizState.confirm)
async def confirm_handler(message:Message,state:FSMContext):
    if message.text == 'Ha':
        await state.update_data(step=0)
        await state.set_state(QuizState.playing)
        await send_questions(message,state)
    else:
        await state.clear()
        await message.answer("Testni boshlash uchun /play ni bosing !")

async def send_questions(message:Message,state:FSMContext):
    data=await state.get_data()
    step=data.get("step",0)

    if step>=len(questions):
        global count_true
        global count_false
        save_to_database(message,count_true,count_false)
        count_true=0
        count_false=0
        await state.clear()
        await message.answer(" Savollar tugadi " , reply_markup=ReplyKeyboardRemove())

        results = results_shower()
        if results:
            text = "\n".join(
                [f"User: {r[0]} | To‘g‘ri: {r[1]} | Noto‘g‘ri: {r[2]}" for r in results if len(r) == 3]
            )

            await message.answer(f"Hozirgacha natijalar:\n{text}")
            await message.answer(
                f"Salom {html.bold(message.from_user.full_name)}!\n\n"
                f"Yana o‘ynashni xohlaysizmi?\nO'yinni boshlash uchun /play ni bosing. 😊",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.clear()
        else:
            await message.answer("Hozirgacha natijalar mavjud emas.")
            await message.answer(
                f"Salom {html.bold(message.from_user.full_name)}!\n\n"
                f"Yana o‘ynashni xohlaysizmi?\nO'yinni boshlash uchun /play ni bosing. 😊",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.clear()

        return
    q=questions[step]
    await  message.answer(q.text,reply_markup=make_keyboard(q.options,rows=2))



count_true=0
count_false=0
@dp.message(QuizState.playing)
async def answer_handler(message:Message, state:FSMContext):
    data= await state.get_data()
    step=  data.get("step",0)
    q=questions[step]
    if message.text == q.correct_answer:
        global count_true
        count_true+=1
        await message.answer("To`g`ri javob ")

    else:
        global count_false
        count_false+=1
        await message.answer(f"Noto`g`ri javob . To'g'ri javob {q.correct_answer}")

    await state.update_data(step=step+1)
    await send_questions(message,state)






async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
