from enum import Enum

from aiogram.filters.callback_data import CallbackData


class CalendarNavigation(Enum):
    forward = "forward"
    back = "back"


class CalendarObj(Enum):
    year = "year"
    month = "month"
    day = "day"


class CalendarCallback(CallbackData, prefix="calendar"):
    year: int
    month: int | None = None
    day: int | None = None
    obj: CalendarObj
    navigation: CalendarNavigation | None = None
