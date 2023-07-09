from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text

from filters.admin_filters import IsFromAdminsChat, AnswerForUser
from lexicon.lexicon_ru import LEXICON_RU

from keyboards.close_button import (confirm_closing_admin_buttons,
                                    confirm_closing_user_buttons)
from services.services import find_user_id_by_chat_id
from database.cache import admins_chats_status, users_dict
from database.database import DataBase


router: Router = Router()
router.message.filter(IsFromAdminsChat())
db = DataBase()


@router.message(AnswerForUser())
async def process_send_answer_to_user(message: Message):
    """В хэндлер попадают апдейты, содержащие сообщения - ответы админов
    на обращения пользователей. Они (ответы админов) должны быть
    доставлены в чат бота с пользователем."""
    user_id = find_user_id_by_chat_id(users_dict, message.chat.id)
    await message.send_copy(user_id)


@router.callback_query(Text(text=['close']))
async def process_close_contacting(callback: CallbackQuery):
    """Ответ на нажатие кнопки "закрыть обращение":
    запрос на подтверждение закрытия."""
    await callback.message.answer(
        text=LEXICON_RU['confirm_closing_admin'],
        reply_markup=confirm_closing_admin_buttons
    )


@router.callback_query(Text(text=['yes_close_admin']))
async def process_confirm_closing(callback: CallbackQuery, bot: Bot):
    """Админ отвечает ДА на запрос подтвердить закрытие обращения.
    Действия бота:
    1) отправляет пользователю информационное сообщение о закрытии обращения
    2) меняет название чата на исходное и его статус на "свободен"
    3) сохраняет данные о теме обращения и времени открытия/закрытия в БД
    4) удаляет данные об обращении из кэша
    5) бросает уведомление о закрытии обращения в чат админов.
    6) НЕ СМОГЛА РЕАЛИЗОВАТЬ: бот должен очищать чат"""
    chat_id = callback.message.chat.id
    user_id = find_user_id_by_chat_id(users_dict, chat_id)

    await bot.send_message(
        user_id,
        LEXICON_RU['confirm_closing_user'],
        reply_markup=confirm_closing_user_buttons
    )
    await bot.set_chat_title(chat_id, LEXICON_RU['default_admin_chat_title'])
    await callback.message.edit_text(LEXICON_RU['is_closed_for_admin'])
    admins_chats_status[str(chat_id)] = 'free'
    tag = users_dict[user_id]['tag']
    date_open = users_dict[user_id]['date_open']
    date_close = callback.message.date
    db.save_data_to_statistic(tag, date_open, date_close)
    del users_dict[user_id]
    await callback.answer(
        f'Обращение по теме {tag} закрыто. Очистите историю чата!',
        show_alert=True
    )


@router.callback_query(Text(text=['no_close_admin']))
async def process_refuse_closing(callback: CallbackQuery):
    """Админ отвечает НЕТ на запрос
    подтвердить делание закрыть обращение."""
    await callback.message.edit_text(LEXICON_RU['no_close'])
