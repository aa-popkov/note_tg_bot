from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.notes import get_main_notes_kb
from utils import states
from utils.kb_data import NotesMenu
from models.user_notes import UserNote

router = Router(name=__name__)


@router.message(StateFilter(states.MainState.notes), F.text == NotesMenu().make_note)
async def create_note(msg: Message, state: FSMContext):
    await msg.answer(
        text="Введи свою заметку 📝"
        "\n\n"
        "<i>Первые 10 символов будут взяты для заголовка заметки.</i>\n"
        "<b>Общий размер заметки не должен превышать 4000 символов!</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(states.NotesState.create_note)


@router.message(StateFilter(states.NotesState.create_note), F.content_type == "text")
async def create_note_get_title(msg: Message, state: FSMContext):

    note = UserNote(
        title=UserNote.convert_title(msg.text),
        text=msg.html_text,
        user_id=str(msg.from_user.id),
    )
    note_id = await UserNote.add_note(note)
    await msg.answer(
        text=f"Заметка успешно создана!\nID заметки: {note_id}",
        reply_markup=get_main_notes_kb(),
    )
    await state.set_state(states.MainState.notes)


@router.message(StateFilter(states.NotesState.create_note), F.content_type != "text")
async def create_note_get_title_non_text(msg: Message, state: FSMContext):
    await msg.reply(text="Заметка пока принимает только текст!")
