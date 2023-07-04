from aiogram.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    choose_tag = State()
    send_first_question = State()
    send_another_question = State()
