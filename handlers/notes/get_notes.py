from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.notes import get_my_notes_kb, get_my_note_kb
from utils import states
from utils.kb_data import NotesMenu
from models.user_notes import UserNote
from models.callback.note import (
    NotesCallback,
    NoteNavigation,
    NoteCallback,
)

router = Router(name=__name__)


@router.message(StateFilter(states.MainState.notes), F.text == NotesMenu().my_notes)
async def get_notes(msg: Message, state: FSMContext):
    notes_count = await UserNote.get_count_by_user(str(msg.from_user.id))
    if notes_count == 0:
        await msg.answer(
            text="Похоже у тебя еще нет заметок😭\n" "Создай новую по кнопке внизу",
        )
        return
    callback_counter = NotesCallback(
        current_page=1,
        next_page=2,
        previous_page=0,
        max_page=((notes_count - 1) // 5) + 1,
    )
    notes = await UserNote.get_all_notes(str(msg.from_user.id))
    await msg.answer(
        text="Твои заметки\n" "Для навигации используй кнопки",
        reply_markup=get_my_notes_kb(notes, callback_counter),
    )


@router.callback_query(NotesCallback.filter())
async def note_callback_forward(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_count = NotesCallback.unpack(callback.data)
    notes_count = await UserNote.get_count_by_user(str(callback.from_user.id))

    note_count.navigate(
        is_forward=note_count.navigation == NoteNavigation.forward,
        notes_count=notes_count,
    )

    notes = await UserNote.get_all_notes(
        str(callback.from_user.id), (note_count.current_page - 1) * 5
    )

    await callback.message.edit_text(
        text=f"Страница #{note_count.current_page}",
        reply_markup=get_my_notes_kb(notes, note_count),
    )


@router.callback_query(NoteCallback.filter())
async def note_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_id = NoteCallback.unpack(callback.data).id
    note = await UserNote.get_note_by_id(str(callback.from_user.id), note_id)
    await callback.message.edit_text(
        text=f"Твоя заметка: <b>{note.title}</b>" f"\n\n" f"{note.text}",
        reply_markup=get_my_note_kb(note_id),
    )
