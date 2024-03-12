from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.kb_data import MainMenu


def get_start_registration_kb() -> ReplyKeyboardMarkup:
    kb_data = MainMenu()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
