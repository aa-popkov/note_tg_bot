from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.start import get_send_contact_kb
from utils import states
from utils.kb_data import StartRegister


router = Router(name=__name__)


@router.message(
    StateFilter(states.StartState.start),
    F.text == StartRegister().register,
)
async def start_register(msg: Message, state: FSMContext):
    await msg.answer(
        text="Твои данные:\n"
        f"ID: {msg.from_user.id}\n"
        f"Username: {msg.from_user.username}\n"
        f"First Name: {msg.from_user.first_name}\n"
        f"Last Name: {msg.from_user.last_name}\n"
        "\n"
        "Для заверешния регистрации отправь свой контакт по кнопке внизу🔽",
        reply_markup=get_send_contact_kb(),
    )
    await state.set_state(states.StartState.start_register)


@router.message(
    StateFilter(states.StartState.start_register),
    F.content_type != ContentType.CONTACT,
    F.text != StartRegister.cancel,
)
async def get_non_contact(msg: Message, state: FSMContext):
    await msg.answer(
        text="🤬 Это не контакт!\n" "Отправь контакт, по кнопке внизу!",
        reply_markup=get_send_contact_kb(),
    )
