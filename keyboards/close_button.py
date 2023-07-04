from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)


keyboard_1: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text='Закрыть обращение', callback_data='close')]]

close_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard_1)



keyboard_2: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text='Да, вопрос закрыт, можно всё удалить', callback_data='yes_close')],
        [InlineKeyboardButton(text='Нет', callback_data='no_close')]
        ]

yes_no_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=keyboard_2)    