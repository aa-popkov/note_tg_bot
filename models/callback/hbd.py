from enum import Enum

from aiogram.filters.callback_data import CallbackData


class HbdNavigation(Enum):
    forward = "forward"
    back = "back"


class HbdType(Enum):
    show_in_msg = "show_in_msg"
    edit_msg = "edit_msg"


class HbdAction(Enum):
    delete = "delete"


class HbdCallback(CallbackData, prefix="hbd"):
    current_page: int
    max_page: int
    navigation: HbdNavigation | None = None
    hbd_type: HbdType = HbdType.show_in_msg


class HbdDeleteCallback(CallbackData, prefix="hbd_edit"):
    id: int
    action: HbdAction | None = None
