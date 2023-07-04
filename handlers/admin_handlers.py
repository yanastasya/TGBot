import datetime

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text

from filters.admin_filters import IsFromAdminsChat, AnswerForUser
from lexicon.lexicon_ru import LEXICON_RU
from database2.database import DataBase
from keyboards.close_button import yes_no_button


db = DataBase()

router: Router = Router()
router.message.filter(IsFromAdminsChat())


@router.message(AnswerForUser())
async def process_send_answer_to_user(message: Message):

    user_id=db.select_user_id_from_cache(message.chat.id)
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
    user_id=int(db.select_user_id_from_cache(chat_id)) 

    await bot.send_message(user_id, LEXICON_RU['is_closed_for_user'])     
    await bot.set_chat_title(chat_id, LEXICON_RU['default_admin_chat_title'])     
    db.change_admin_chat_status_to_free(chat_id)   
    
    tag = db.select_tag_from_cache(user_id) 
    date_open = db.select_date_open_from_cache(user_id)    
    
    date_close_datetime = callback.message.date
    date_close_str = date_close_datetime.strftime("%Y-%m-%d %H:%M:%S")
    date_close = datetime.datetime.strptime(date_close_str, '%Y-%m-%d %H:%M:%S')
    application_review_time = date_close - date_open
    print(application_review_time)
    db.save_data_to_statistic(tag, str(application_review_time))

    await callback.answer(
        f'Обращение по теме {tag} рассмотрено за {application_review_time}'
        f'Молодцы! Можно очистить чат!',
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