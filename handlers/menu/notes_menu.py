from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import states
from keyboards.notes import get_main_notes_kb
from utils.kb_data import MainMenu

router = Router(name=__name__)


@router.message(Command("notes"))
@router.message(StateFilter(states.MainState.menu), F.text == MainMenu().notes)
async def notes_menu(msg: Message, state: FSMContext):
    await msg.reply(
        text="Можно создать себе заметку или посмотреть существующую\n"
        "Воспользуйся клавиатурой внизу",
        reply_markup=get_main_notes_kb(),
    )
    await state.set_state(states.MainState.notes)
