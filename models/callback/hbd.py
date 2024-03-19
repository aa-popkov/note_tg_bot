from enum import Enum

from aiogram.filters.callback_data import CallbackData


class HbdNavigation(Enum):
    forward = "forward"
    back = "back"


class HbdCallback(CallbackData, prefix="hbd"):
    current_page: int
    max_page: int
    navigation: HbdNavigation | None = None
