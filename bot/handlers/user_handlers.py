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
from FSM.fsm import FSMUser
from database.cache import admins_chats_status, users_dict
from services.services import choose_free_admin_chat

load_dotenv()
router: Router = Router()


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """Ответ на команду help."""
    await message.answer(text=LEXICON_RU['/help'])


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    """Ответ на команду start: кнопки с выбором темы обращения.
    И изменение состояния на ожидание выбора тэга."""
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=tags_choose_keyboard)
    await state.set_state(FSMUser.choose_tag)


@router.message(
        Command(commands='cancel'),
        StateFilter(FSMUser.send_first_question)
)
async def process_cancel_command(message: Message, state: FSMContext):
    """Ответ на команду cancel: можно отменить выбор тэга
    и начать заново с команды start """
    await message.answer(text=LEXICON_RU['/cancel'])
    await state.clear()


@router.message(
        Command(commands='cancel'),
        StateFilter(default_state, FSMUser.choose_tag)
)
async def process_cancel_nothing(message: Message):
    """Если команда cancel быыла отправлена до выбора темы обращения,
    то пользователь получает сообщение о том, что отменять нечего"""
    await message.answer(text=LEXICON_RU['/cancel_nothing'])


@router.message(
        Command(commands='cancel'),
        ~StateFilter(default_state, FSMUser.choose_tag)
)
async def process_cancel_impossible(message: Message):
    """Если оманда cancel быыла отправлена уже после отправки
    сообщения админам, то отмена невозможна. Пользователь получает
    сообщение об этом."""
    await message.answer(text=LEXICON_RU['/cancel_impossible'])


@router.callback_query(
        StateFilter(FSMUser.choose_tag),
        Text(text=['Платформа', 'Сотрудничество', 'Баги', 'Другое']))
async def process_choose_tag(callback: CallbackQuery, state: FSMContext):
    """Ответ пользовалю после выбора им темы обращения.
    Изменение состояния на ожидание вопроса от пользователя."""
    await state.update_data(tag=callback.data)
    await callback.message.edit_text(
        text=LEXICON_RU['choose_tag'],
    )
    await state.set_state(FSMUser.send_first_question)


@router.message(StateFilter(FSMUser.choose_tag))
async def warning_not_tag(message: Message):
    """Ответ пользователю в случае ,если вместо выбота темы
    с помощью нажатия на кнопку, он делает что-то другое"""
    await message.answer(text=LEXICON_RU['warning_not_tag'])


@router.message(StateFilter(FSMUser.send_first_question))
async def process_send_first_question(
    message: Message, bot: Bot, state: FSMContext
):
    """Первое сообщение с вопросом от пользователя.
    Действия бота:
    1) выбирает свободный чат или дополнительный чат,
    если свободных нет
    2) в чате администраторов появляются сообщения
    о том, что поступило новое обращение и копия сообщения
    пользователя + кнопка "закрыть обращение"
    3) название чата меняется на тему обращения
    4) пользователь получает уведомление о том, что его
    обращение принято

    Состояние меняется на ожидание следующих сообщений
    от пользователя.
    """
    chat_id = (choose_free_admin_chat(admins_chats_status))
    if chat_id is not None:
        admins_chats_status[str(chat_id)] = 'not_free'
    else:
        chat_id = os.getenv('ADMINS_EXTRA_CHAT')

    state_data = await state.get_data()
    tag = state_data['tag']
    await state.update_data(admin_chat_id=int(chat_id))
    await state.update_data(date_open=message.date)

    users_dict[message.chat.id] = await state.get_data()

    message_text = (
        f"\U00002757 Поступило новое обращение \U00002757\n"
        f"<b>Тема:</b> {tag}\n "
        f"<b>От кого</b>:\n"
        f"username: {message.chat.username}\n"
        f"( {message.chat.first_name} "
        f" {message.chat.last_name} )"
        f"\U0001F447\U0001F447\U0001F447<b>содержание</b>"
        f"\U0001F447\U0001F447\U0001F447"

    )
    chat_title = f"{tag}"

    await bot.set_chat_title(chat_id, chat_title)
    await bot.send_message(chat_id, message_text)
    await message.send_copy(chat_id, reply_markup=close_button)
    await message.answer(LEXICON_RU['send_first_question'])
    await state.set_state(FSMUser.send_another_question)


@router.message((StateFilter(FSMUser.send_another_question)))
async def process_not_first_sms(message: Message, state: FSMContext):
    """Все сообщения от пользователя, кроме самого первого,
    просто пересылаются в чат администраторов."""
    chat_id = (await state.get_data())['admin_chat_id']
    await message.forward(chat_id)


@router.callback_query(
        StateFilter(FSMUser.send_another_question),
        Text(text=['yes_close_user']))
async def process_yes_close_user(callback: CallbackQuery, state: FSMContext):
    """Ответ пользователя ДА на вопрос после закрытия обращения.
    Нужно для того, чтобы сбросить состояние."""
    await callback.message.edit_text(LEXICON_RU['is_closed_for_user_yes'])
    await state.clear()


@router.callback_query(
        StateFilter(FSMUser.send_another_question),
        Text(text=['no_close_user']))
async def process_no_close_user(callback: CallbackQuery, state: FSMContext):
    """Ответ пользователя ДА на вопрос после закрытия обращения.
    Нужно для того, чтобы сбросить состояние."""
    await callback.message.edit_text(LEXICON_RU['is_closed_for_user_no'])
    await state.clear()
