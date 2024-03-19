from datetime import date
from calendar import monthcalendar

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from models.callback.hbd import HbdCallback, HbdNavigation
from utils.kb_data import HbdMenu
from models.callback.calendar import CalendarCallback, CalendarNavigation, CalendarObj


months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def get_hbd_kb() -> ReplyKeyboardMarkup:
    kb_data = HbdMenu()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_hbd_year_calendar(year: int | None = date.today().year) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for button in range(-7, 1):
        builder.add(
            InlineKeyboardButton(
                text=str(year + button),
                callback_data=CalendarCallback(
                    year=year + button,
                    obj=CalendarObj.year,
                ).pack(),
            )
        )
    builder.add(
        InlineKeyboardButton(
            text="<<",
            callback_data=CalendarCallback(
                navigation=CalendarNavigation.back,
                year=year,
                obj=CalendarObj.year,
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=">>",
            callback_data=CalendarCallback(
                navigation=CalendarNavigation.forward,
                year=year,
                obj=CalendarObj.year,
            ).pack(),
        )
    )
    builder.adjust(4, 4, 2)
    return builder.as_markup()


def get_hbd_month_calendar(
    cb: CalendarCallback,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i, month in enumerate([months[i] for i in range(0, 12)]):
        builder.add(
            InlineKeyboardButton(
                text=month,
                callback_data=CalendarCallback(
                    year=cb.year,
                    month=i,
                    obj=CalendarObj.month,
                ).pack(),
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="<<",
            callback_data=CalendarCallback(
                year=cb.year,
                navigation=CalendarNavigation.back,
                obj=CalendarObj.month,
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=str(cb.year),
            callback_data=CalendarCallback(
                year=cb.year,
                obj=CalendarObj.month,
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=">>",
            callback_data=CalendarCallback(
                year=cb.year,
                navigation=CalendarNavigation.forward,
                obj=CalendarObj.month,
            ).pack(),
        )
    )
    builder.adjust(3)
    return builder.as_markup()


def get_hbd_day_calendar(
    cb: CalendarCallback,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="<<",
            callback_data=CalendarCallback(
                year=cb.year,
                month=cb.month,
                obj=CalendarObj.day,
                navigation=CalendarNavigation.back,
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=f"{months[cb.month]} {cb.year}",
            callback_data=CalendarCallback(
                year=cb.year,
                obj=CalendarObj.year,
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=">>",
            callback_data=CalendarCallback(
                year=cb.year,
                month=cb.month,
                obj=CalendarObj.day,
                navigation=CalendarNavigation.forward,
            ).pack(),
        )
    )

    days = monthcalendar(cb.year, cb.month + 1)

    for weekday in weekdays:
        builder.add(InlineKeyboardButton(text=weekday, callback_data=" "))

    for week in days:
        for day in week:
            builder.add(
                InlineKeyboardButton(
                    text=str(day) if day != 0 else " ",
                    callback_data=(
                        CalendarCallback(
                            year=cb.year,
                            month=cb.month,
                            day=day,
                            obj=CalendarObj.day,
                        ).pack()
                        if day != 0
                        else " "
                    ),
                )
            )

    builder.adjust(3, 7)
    return builder.as_markup()


def get_hbd_in_msg_kb(cb: HbdCallback) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if cb.current_page+1 != 1:
        builder.add(
            InlineKeyboardButton(
                text="<<",
                callback_data=HbdCallback(
                    current_page=cb.current_page - 1,
                    max_page=cb.max_page,
                    navigation=HbdNavigation.back,
                ).pack(),
            )
        )

    builder.add(
        InlineKeyboardButton(
            text=f"{cb.current_page+1}/{cb.max_page}", callback_data=" "
        )
    )

    if cb.current_page+1 != cb.max_page:
        builder.add(
            InlineKeyboardButton(
                text=">>",
                callback_data=HbdCallback(
                    current_page=cb.current_page + 1,
                    max_page=cb.max_page,
                    navigation=HbdNavigation.back,
                ).pack(),
            )
        )

    return builder.as_markup()
