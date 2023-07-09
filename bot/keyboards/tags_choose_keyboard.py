from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Платформа \U0001F4BB',
    callback_data='Платформа')

button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Сотрудничество \U0001F37B',
    callback_data='Сотрудничество')

button_3: InlineKeyboardButton = InlineKeyboardButton(
    text='Баги \U00002049',
    callback_data='Баги')

button_4: InlineKeyboardButton = InlineKeyboardButton(
    text='Другое \U0001F609',
    callback_data='Другое')

tags_choose_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_1],
                     [button_2],
                     [button_3],
                     [button_4]]
    )
