from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard_1: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text='Закрыть обращение \U0000274C', callback_data='close'
            )]]

close_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard_1)


keyboard_2: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text='Да \U00002714',
            callback_data='yes_close_admin'
            )],
        [InlineKeyboardButton(
            text='Нет \U0000274C', callback_data='no_close_admin'
        )]
        ]

confirm_closing_admin_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard_2)


keyboard_3: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(
            text='Да, спасибо!', callback_data='yes_close_user'
            )],
        [InlineKeyboardButton(
            text='Нет, хочу задать еще вопрос.', callback_data='no_close_user'
            )]
        ]

confirm_closing_user_buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard_3)
