from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import states
from keyboards.main_menu import get_start_registration_kb

router = Router(name=__name__)


@router.message(Command("menu"))
@router.message(StateFilter(states.MainState.main))
async def main_menu(msg: Message, state: FSMContext):
    await msg.answer(
        text="🏠Главное меню\n" "Для навигации используйте кнопки внизу",
        reply_markup=get_start_registration_kb(),
    )
    await state.set_state(states.MainState.menu)
