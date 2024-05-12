from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

create = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать новую дату', callback_data='create_date')]
])