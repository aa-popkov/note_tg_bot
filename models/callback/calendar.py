from enum import Enum

from aiogram.filters.callback_data import CallbackData


class CalendarNavigation(Enum):
    forward = "forward"
    back = "back"


class CalendarCallback(CallbackData, prefix="calendar"):
    year: int
    navigation: CalendarNavigation | None = None
