from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ContentType

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
        "<b>Общий размер заметки не должен превышать 1000 символов!</b>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(states.NotesState.create_note)


@router.message(StateFilter(states.NotesState.create_note), F.content_type == "text")
async def create_note_get_title(msg: Message, state: FSMContext):
    if len(msg.text) > 1000:
        await msg.answer("Текст заметки превышает 1000 символов!\nПопробуй еще раз")
        return
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


@router.message(
    StateFilter(states.NotesState.create_note), F.content_type == ContentType.PHOTO
)
async def create_note_get_title_non_text(msg: Message, state: FSMContext):
    if msg.caption is None:
        await msg.answer("Текст заметки должен содержать <b>хоть какой-то текст</b>!\nПопробуй еще раз")
        return
    if len(msg.caption) > 1000:
        await msg.answer("Текст заметки превышает 1000 символов!\nПопробуй еще раз")
        return
    note = UserNote(
        title=UserNote.convert_title(msg.caption),
        text=msg.html_text,
        user_id=str(msg.from_user.id),
        file_id=msg.photo[-1].file_id
    )
    note_id = await UserNote.add_note(note)
    await msg.answer(
        text=f"Заметка успешно создана!\nID заметки: {note_id}",
        reply_markup=get_main_notes_kb(),
    )
    await state.set_state(states.MainState.notes)
