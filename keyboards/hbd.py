from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.kb_data import HbdMenu


def get_hbd_kb() -> ReplyKeyboardMarkup:
    kb_data = HbdMenu()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
