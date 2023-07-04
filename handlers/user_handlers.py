import os

from dotenv import load_dotenv
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.tags_choose_keyboard import tags_choose_keyboard
from keyboards.close_button import close_button
from bot import DataBase

from filters.user_filters import IsFromUser
from errors.errors import NotFreeChatsException
from FSM.fsm import FSMUser

load_dotenv()
router: Router = Router()
router.message.filter(IsFromUser())

db = DataBase()


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=tags_choose_keyboard)
    await state.set_state(FSMUser.choose_tag)


@router.message(Command(commands='cancel'), StateFilter(FSMUser.send_first_question))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'])    
    await state.clear()


@router.message(Command(commands='cancel'), StateFilter(default_state, FSMUser.choose_tag))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['/cancel_nothing']) 
      

@router.message(Command(commands='cancel'), ~StateFilter(default_state, FSMUser.choose_tag))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel_impossible'])


@router.callback_query(
        StateFilter(FSMUser.choose_tag),
        Text(text=['Платформа', 'Сотрудничество', 'Баги', 'Другое']))
async def process_choose_tag(callback: CallbackQuery, state: FSMContext):
    await state.update_data(tag=callback.data)        
    await callback.message.edit_text(
        text=LEXICON_RU['choose_tag'],
    )
    await state.set_state(FSMUser.send_first_question)


@router.message(StateFilter(FSMUser.choose_tag))
async def warning_not_tag(message: Message):
    await message.answer(text=LEXICON_RU['warning_not_tag'])


@router.message(StateFilter(FSMUser.send_first_question))
async def process_send_first_question(message: Message, bot: Bot, state: FSMContext):
    try:
        chat_id = int(db.choose_free_admin_chat())
        db.change_admin_chat_status_to_not_free(chat_id)
    except NotFreeChatsException:
        chat_id = os.getenv('ADMINS_EXTRA_CHAT')
    
    user_id = message.chat.id
    date_open = message.date.strftime("%Y-%m-%d %H:%M:%S")
    state_data = await state.get_data()
    tag = state_data['tag']

    db.save_data_to_cache(user_id, chat_id, tag, date_open)

    await state.update_data(admin_chat_id=chat_id)
    #await state.update_data(date_open=message.date)
    #user_dict[message.chat.id] = await state.get_data() здесь достаточно и лучше сохранить в кэш в виде словаря,
    # но я использую таблицу cache в постоянном хранилище, потому что не могу разобраться с redis...    

    message_text = (
        f"Поступило новое обращение!"
        f"Тема: {tag} "
    )
    chat_title = f"{tag}"

    await bot.set_chat_title(chat_id, chat_title)
    await bot.send_message(chat_id, message_text)        
    await message.send_copy(chat_id, reply_markup=close_button)
    await state.set_state(FSMUser.send_another_question)


@router.message((StateFilter(FSMUser.send_another_question)))
async def process_not_first_sms(message: Message, state: FSMContext):
    chat_id = (await state.get_data())['admin_chat_id']
    await message.forward(chat_id, reply_markup=close_button)


#@router.message()
#async def answer_if_not_admins_update(message: Message, state: FSMContext):
 #   print((await state.get_data()))  
 #   await message.answer(text='Это сообщение прошло сквозь все фильтры юзеров')
