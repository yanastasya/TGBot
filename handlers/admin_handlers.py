from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text

from filters.admin_filters import IsFromAdminsChat, AnswerForUser
from lexicon.lexicon_ru import LEXICON_RU

from keyboards.close_button import yes_no_button
from services.services import find_user_id_by_chat_id
from database.cache import admins_chats_status,users_dict
from database.database import DataBase


router: Router = Router()
router.message.filter(IsFromAdminsChat())
db = DataBase()

@router.message(AnswerForUser())
async def process_send_answer_to_user(message: Message):

    user_id = find_user_id_by_chat_id(users_dict, message.chat.id)
    await message.send_copy(user_id)


@router.callback_query(Text(text=['close']))
async def process_close_contacting(callback: CallbackQuery):
    await callback.message.answer(
        text=LEXICON_RU['confirm_closing'],
        reply_markup=yes_no_button
    )


@router.callback_query(Text(text=['yes_close']))
async def process_confirm_closing(callback: CallbackQuery, bot: Bot):
    chat_id = callback.message.chat.id    
    user_id=find_user_id_by_chat_id(users_dict, chat_id)

    await bot.send_message(user_id, LEXICON_RU['is_closed_for_user'])     
    await bot.set_chat_title(chat_id, LEXICON_RU['default_admin_chat_title'])     

    admins_chats_status[str(chat_id)]='free'

    tag = users_dict[user_id]['tag']
    date_open = users_dict[user_id]['date_open']
    date_close = callback.message.date    
    
    db.save_data_to_statistic(tag, date_open, date_close)
    del users_dict[user_id]    

    await callback.answer(
        f'Обращение по теме {tag} закрыто. Очистите историю чата!',       
        show_alert=True
    )

@router.callback_query(Text(text=['no_close']))
async def process_refute_closing(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON_RU['no_close'])


#@router.message()
#async def answer_if_not_admins_update(message: Message, state: FSMContext):
   # print(message.json(indent=4, exclude_none=True))
   # print(await state.get_data())           
   # await message.answer(text='')