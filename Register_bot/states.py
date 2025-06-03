from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery


class ChangeEmailState(StatesGroup):
    email = State()


class ChangePhoneState(StatesGroup):
    phone = State()

class ChangeAddressState(StatesGroup):
        address= State()

class AddUserState(StatesGroup):
    first_name= State()
    last_name= State()
    email= State()
    phone= State()
    address= State()
    chat_id= State()
    username= State()


class Chat_idState(StatesGroup):
    chat_id= State()

