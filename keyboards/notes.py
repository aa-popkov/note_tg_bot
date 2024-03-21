from typing import List

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from models.user_notes import UserNote
from schemas.callback.note import (
    NotesCallback,
    NoteNavigation,
    NoteCallback,
    NoteActionCallback,
    NoteAction,
)
from utils.kb_data import NotesMenu, NoteEdit


def get_main_notes_kb() -> ReplyKeyboardMarkup:
    kb_data = NotesMenu()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_edit_note_kb() -> ReplyKeyboardMarkup:
    kb_data = NoteEdit()
    builder = ReplyKeyboardBuilder()
    for button in kb_data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_my_notes_kb(
    notes: List[UserNote], notes_callback: NotesCallback
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    notes_rows = builder.row(width=1)
    for note in notes:
        notes_rows.add(
            InlineKeyboardButton(
                text=note.title, callback_data=NoteCallback(id=note.id).pack()
            )
        )
    builder.adjust(1)

    cb_f = notes_callback.model_copy(update={"navigation": NoteNavigation.forward})
    cb_b = notes_callback.model_copy(update={"navigation": NoteNavigation.back})

    nav_button = []

    if notes_callback.previous_page != 0:
        nav_button.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=cb_b.pack(),
            )
        )

    nav_button.append(
        InlineKeyboardButton(
            text=f"{notes_callback.current_page}/{notes_callback.max_page}",
            callback_data="None",
        )
    )

    if notes_callback.max_page != notes_callback.current_page:
        nav_button.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=cb_f.pack(),
            )
        )

    builder.row(*nav_button, width=len(nav_button))

    return builder.as_markup()


def get_my_note_kb(note_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="✍️ Изменить",
            callback_data=NoteActionCallback(id=note_id, action=NoteAction.edit).pack(),
        ),
        InlineKeyboardButton(
            text="❌ Удалить",
            callback_data=NoteActionCallback(
                id=note_id, action=NoteAction.delete
            ).pack(),
        ),
    )
    return builder.as_markup()
