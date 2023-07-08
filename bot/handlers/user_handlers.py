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


from filters.user_filters import IsFromUser
from errors.errors import NotFreeChatsException
from FSM.fsm import FSMUser
from database.cache import admins_chats_status, users_dict
from services.services import choose_free_admin_chat

load_dotenv()
router: Router = Router()
router.message.filter(IsFromUser())




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
async def process_cancel_command(message: Message):
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
    chat_id = (choose_free_admin_chat(admins_chats_status))
    if not chat_id==None:
        admins_chats_status[str(chat_id)] = 'not_free'
    else:    
        chat_id = os.getenv('ADMINS_EXTRA_CHAT')    
    
    state_data = await state.get_data()
    tag = state_data['tag']    

    await state.update_data(admin_chat_id=int(chat_id))
    await state.update_data(date_open=message.date)
    
    users_dict[message.chat.id] = await state.get_data()

    message_text = (
        f"Поступило новое обращение!"
        f"Тема: {tag} "
    )
    chat_title = f"{tag}"

    await bot.set_chat_title(chat_id, chat_title)
    await bot.send_message(chat_id, message_text)        
    await message.send_copy(chat_id, reply_markup=close_button)
    await message.answer(LEXICON_RU['send_first_question'])
    await state.set_state(FSMUser.send_another_question)


@router.message((StateFilter(FSMUser.send_another_question)))
async def process_not_first_sms(message: Message, state: FSMContext):
    chat_id = (await state.get_data())['admin_chat_id']
    await message.forward(chat_id, reply_markup=close_button)


@router.callback_query(
        StateFilter(FSMUser.send_another_question),
        Text(text=['yes_close_user']))
async def process_choose_tag(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['is_closed_for_user_yes'])
    await state.clear()


@router.callback_query(
        StateFilter(FSMUser.send_another_question),
        Text(text=['no_close_user']))
async def process_choose_tag(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['is_closed_for_user_no'])
    await state.clear()




