from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.kb_data import CatsMenu


def get_main_cats_kb() -> ReplyKeyboardMarkup:
    kb_data = CatsMenu()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
