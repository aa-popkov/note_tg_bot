from enum import Enum
from typing import NoReturn

from aiogram.filters.callback_data import CallbackData


class NoteNavigation(Enum):
    forward = "forward"
    back = "back"


class NotesCallback(CallbackData, prefix="notes_"):
    navigation: NoteNavigation | None = None
    current_page: int
    next_page: int
    previous_page: int
    max_page: int

    def navigate(self, is_forward: bool, notes_count: int) -> NoReturn:
        if is_forward:
            self.current_page += 1
            self.next_page += 1
            self.previous_page += 1
            self.max_page = ((notes_count - 1) // 5) + 1
        else:
            self.current_page -= 1
            self.next_page -= 1
            self.previous_page -= 1
            self.max_page = ((notes_count - 1) // 5) + 1


class NoteCallback(CallbackData, prefix="note_"):
    id: int


class NoteAction(Enum):
    edit = "edit"
    delete = "delete"


class NoteActionCallback(CallbackData, prefix="noteaction_"):
    id: int
    action: NoteAction
