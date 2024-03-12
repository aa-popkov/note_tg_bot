from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter

from handlers.start.registration import start_register
from keyboards.start import get_start_registration_kb
from utils.kb_data import StartRegister
from utils import states

router = Router(name=__name__)


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await msg.answer(
        text="👋Привет!\n"
        "🙆Для использования бота необходимо пройти регистрацию.\n"
        "Воспользуйся кнопкой внизу",
        reply_markup=get_start_registration_kb(),
    )
    await state.set_state(states.StartState.start)


@router.message(StateFilter(states.StartState), F.text == StartRegister().cancel)
async def cancel(msg: Message, state: FSMContext):
    await msg.answer(
        text="😭 Очень жаль...\n"
        "Для повторной регистрации воспользуйся командой:\n"
        "/start\n"
        "\n"
        "Или напиши мне любое сообщение 🙋‍♂️",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(states.StartState.cancel_register)


@router.message(StateFilter(states.StartState.cancel_register))
async def cancel_state(msg: Message, state: FSMContext):
    await start_register(msg, state)
