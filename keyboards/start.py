from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.kb_data import SendContact, StartRegister


def get_start_registration_kb() -> ReplyKeyboardMarkup:
    kb_data = StartRegister()
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=kb_data.register))
    builder.add(KeyboardButton(text=kb_data.cancel))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_send_contact_kb() -> ReplyKeyboardMarkup:
    kb_data = SendContact()
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=kb_data.send, request_contact=True))
    builder.add(KeyboardButton(text=kb_data.cancel))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
