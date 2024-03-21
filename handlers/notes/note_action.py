from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.notes import get_my_notes_kb, get_edit_note_kb, get_main_notes_kb
from schemas.callback.note import NoteActionCallback, NoteAction, NotesCallback
from models.user_notes import UserNote
from utils import states
from utils.states import NotesState
from utils.bot import bot

router = Router(name=__name__)


@router.callback_query(NoteActionCallback.filter(F.action == NoteAction.delete))
async def note_action_delete_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_id = NoteActionCallback.unpack(callback.data).id
    delete_result = await UserNote.delete_note(note_id)

    notes_count = await UserNote.get_count_by_user(str(callback.from_user.id))
    callback_counter = NotesCallback(
        current_page=1,
        next_page=2,
        previous_page=0,
        max_page=(notes_count // 5) + 1,
    )
    notes = await UserNote.get_all_notes_by_user(str(callback.from_user.id))
    try:
        await callback.message.delete()
    except Exception as e:
        if len(notes) > 0:
            await callback.message.edit_text(
                text=f"Заметка удалена",
                reply_markup=get_my_notes_kb(notes, callback_counter),
            )
        else:
            await callback.message.edit_text(
                text="У тебя больше не осталось заметок\n"
                     "\n"
                     "📝 В меню заметок: /notes\n"
                     "🏠 В главное меню: /menu",
                reply_markup=None
            )
        return
    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text="Заметка удалена",
        reply_markup=get_main_notes_kb()
    )


@router.callback_query(NoteActionCallback.filter(F.action == NoteAction.edit))
async def note_action_edit_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_id = NoteActionCallback.unpack(callback.data).id
    note = await UserNote.get_note_by_id(str(callback.from_user.id), note_id)
    await state.set_state(NotesState.edit_note)
    await state.set_data({"note_id": note.id})
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"Вот твоя заметка: <b>{note.title}</b>\n"
        f"<i>Для редактирования скопируй её и отправь заново</i>\n"
        f"Для отмены воспользуйся кнопкой внизу\n\n"
        f"{note.text}",
        reply_markup=get_edit_note_kb(),
    )
    await callback.message.delete()


@router.message(StateFilter(states.NotesState.edit_note), F.content_type != "text")
async def note_action_edit_non_text(message: Message, state: FSMContext):
    await message.reply(
        text="Похоже, что это не текст!\n"
        "Заметки принимают только текст, попробуй еще раз!",
        reply_markup=get_edit_note_kb(),
    )


@router.message(StateFilter(states.NotesState.edit_note), F.content_type == "text")
async def note_action_edit_text(message: Message, state: FSMContext):
    note_id = (await state.get_data())["note_id"]
    note = await UserNote.get_note_by_id(str(message.from_user.id), note_id)
    note.text = message.text
    note.title = UserNote.convert_title(message.text)
    await UserNote.update_note(note)
    await state.set_state(states.MainState.notes)
    await message.answer(
        text="Заметка обновлена",
        reply_markup=get_main_notes_kb(),
    )
