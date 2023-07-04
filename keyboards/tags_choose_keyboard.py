from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TAGS = {
    'Сотрудничество': 'cooperation',
    'Баги': 'bags',
    'Платформа': 'platform',
    'Другое': 'other'
}

button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Платформа',
    callback_data='Платформа')

button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Сотрудничество',
    callback_data='Сотрудничество')

button_3: InlineKeyboardButton = InlineKeyboardButton(
    text='Баги',
    callback_data='Баги')

button_4: InlineKeyboardButton = InlineKeyboardButton(
    text='Другое',
    callback_data='Другое')

tags_choose_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_1],
                     [button_2],
                     [button_3],
                     [button_4]]
    )