from os import getenv

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from dotenv import load_dotenv

from Register_bot.ORM import Users
from Register_bot.main_app import main_menu, update
from Register_bot.states import ChangeEmailState, ChangePhoneState, ChangeAddressState, AddUserState, Chat_idState

load_dotenv()
ADMIN = list(map(int, getenv('ADMIN').split(',')))
callback_router = Router()
us = Users()


@callback_router.message(CommandStart())
async def start_cmd(message: Message):
    is_admin = message.chat.id in ADMIN
    await us.create_or_update_user({
        "chat_id": message.chat.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username,
    })
    await message.answer("Xush kelibsiz! Quyidagi menyudan foydalaning:", reply_markup=main_menu(is_admin))


@callback_router.message(F.text == "/Registration")
async def start_cmd(message: Message):
    is_admin = message.chat.id in ADMIN
    await us.create_or_update_user({
        "chat_id": message.chat.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username,
    })
    await message.answer("Ro'yhatdan o'tdingiz ! Quyidagi menyudan foydalaning:", reply_markup=main_menu(is_admin))


@callback_router.callback_query(F.data == "view_me")
async def view_me(call: CallbackQuery):
    user = await us.get_by_chat_id(call.message.chat.id)
    if user:
        user_data = (
            f"👤 <b>Foydalanuvchi ma'lumotlari:</b>\n"
            f"📛 Ism: {user.first_name or 'Noma’lum'}\n"
            f"👤 Familiya: {user.last_name or 'Noma’lum'}\n"
            f"🔐 Username: @{user.username or 'Yo‘q'}\n"
            f"📱 Telefon: {user.phone or 'Yo‘q'}\n"
            f"📧 Email: {user.email or 'Yo‘q'}\n"
            f"🏠 Manzil: {user.address or 'Yo‘q'}"
        )
        await call.message.answer(user_data, parse_mode="HTML")

    else:
        await call.message.answer("Ma'lumot topilmadi.")


@callback_router.callback_query(F.data == "delete_user")
async def delete_me(call: CallbackQuery, state: FSMContext):
    await state.set_state(Chat_idState.chat_id)
    await call.message.answer("Foydalanuvchi chat_id sini kiriting:")


@callback_router.message(Chat_idState.chat_id)
async def delete_user(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.text)
    data = await state.get_data()
    chat_id = data.get("chat_id")

    user = await us.get_by_chat_id(chat_id)
    if user:
        await us.delete(chat_id)
        await message.answer("👌 Ma'lumotlar o'chirildi!")
    else:
        await message.answer("🤦‍ Ma'lumot topilmadi !")


@callback_router.callback_query(F.data == "delete_user")
async def delete_me(call: CallbackQuery):
    user = await us.get_by_chat_id(call.message.chat.id)
    if user:
        await us.delete(call.message.chat.id)
        await call.message.answer("🤦‍♀️ Ma'lumotlar o'chirildi!")
    else:
        await call.message.answer("🤦‍ Ma'lumot topilmadi !")


@callback_router.callback_query(F.data == "update_me")
async def update_me(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🤔 Qaysi ma'lumotni o'zgartiramiz ? \n"
                              "Tanlang=>", reply_markup=update())


@callback_router.callback_query(F.data == "email")
async def update_email(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(ChangeEmailState.email)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer("😊Yangi email ni yuboring ", reply_markup=ReplyKeyboardRemove())


@callback_router.message(ChangeEmailState.email)
async def update_email(message: Message, state: FSMContext):
    updated = await us.update(chat_id=message.chat.id, email=message.text)
    if updated:
        await message.answer(" 😊Email muvaffaqqiyatli o'zgartirildi ! ")
    else:
        await message.answer("❌ Emailni yangilashda xatolik yuz berdi.")

    await state.clear()


@callback_router.callback_query(F.data == "phone")
async def update_phone(call: CallbackQuery, state: FSMContext):
    await state.set_state(ChangePhoneState.phone)
    await call.message.answer("😊Yangi Telefon raqamni yuboring ")


@callback_router.message(ChangePhoneState.phone)
async def update_phone(message: Message, state: FSMContext):
    updated = await us.update(chat_id=message.chat.id, phone=message.text)
    if updated:
        await message.answer(" 📱Telefon raqam muvaffaqqiyatli o'zgartirildi !")
    else:
        await message.answer("❌ Raqamni yangilashda xatolik yuz berdi.Ma'lumotlar o'chirilgan /Registration")

    await state.clear()


@callback_router.callback_query(F.data == "address")
async def update_address(call: CallbackQuery, state: FSMContext):
    await state.set_state(ChangeAddressState.address)
    await call.message.answer("😊 Yangi Manzilni yuboring ")


@callback_router.message(ChangeAddressState.address)
async def update_address(message: Message, state: FSMContext):
    updated = await us.update(chat_id=message.chat.id, address=message.text)
    if updated:
        await message.answer(" 📃 Manzil muvaffaqqiyatli o'zgartirildi !")
    else:
        await message.answer("❌ Manzilni yangilashda xatolik yuz berdi.")

    await state.clear()


@callback_router.callback_query(F.data == "view_users")
async def view_users(call: CallbackQuery):
    users = await us.get_all()
    if not users:
        await call.message.answer("🤔 Hech qanday foydalanuvchi topilmadi !")
    else:
        text = " <b>📋 Foydalanuvchilar ro'yxati:</b>\n\n"
        for username, chat_id in enumerate(users, 1):
            text += f" 👤 <b>@{username or 'Noma’lum'}</b> — <code>{chat_id}</code>\n"

        await call.message.answer(text, parse_mode="HTML")


@callback_router.callback_query(F.data == "add_user")
async def add_user(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ismni kiriting=>")
    await state.set_state(AddUserState.first_name)


@callback_router.message(AddUserState.first_name)
async def fist_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Familiyani kiriting:")
    await state.set_state(AddUserState.last_name)


@callback_router.message(AddUserState.last_name)
async def last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Emailni kiriting:")
    await state.set_state(AddUserState.email)


@callback_router.message(AddUserState.email)
async def email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Telefon raqamni kiriting:")
    await state.set_state(AddUserState.phone)


@callback_router.message(AddUserState.phone)
async def phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(" Manzilni kiriting:")
    await state.set_state(AddUserState.address)


@callback_router.message(AddUserState.address)
async def address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Chat_id ni kiriting:")
    await state.set_state(AddUserState.chat_id)


@callback_router.message(AddUserState.chat_id)
async def chat_idd(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.text)
    await message.answer("Username ni kiriting:")
    await state.set_state(AddUserState.username)


@callback_router.message(AddUserState.username)
async def username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    data = await state.get_data()
    email = data.get("email")
    phone = data.get("phone")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    address = data.get("address")
    chat_id = data.get("chat_id")
    username = data.get("username")
    await us.add_user(phone=phone, email=email, first_name=first_name, last_name=last_name, address=address,
                      chat_id=chat_id, username=username)
    await state.clear()
