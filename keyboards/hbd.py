from datetime import date

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from utils.kb_data import HbdMenu
from models.callback.calendar import CalendarCallback, CalendarNavigation


def get_hbd_kb() -> ReplyKeyboardMarkup:
    kb_data = HbdMenu()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_hbd_calendar(year: int | None = date.today().year) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for button in range(-7, 1):
        builder.add(
            InlineKeyboardButton(
                text=str(year + button),
                callback_data=CalendarCallback(year=button).pack(),
            )
        )
    builder.add(
        InlineKeyboardButton(
            text="<<",
            callback_data=CalendarCallback(
                navigation=CalendarNavigation.back, year=year
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=">>",
            callback_data=CalendarCallback(
                navigation=CalendarNavigation.forward, year=year
            ).pack(),
        )
    )
    builder.adjust(4, 4, 2)
    return builder.as_markup()
