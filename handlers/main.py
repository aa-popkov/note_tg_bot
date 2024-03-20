from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils import states

router = Router(name=__name__)


@router.message(StateFilter(states.MainState.wait_operation))
async def wait_operation(message: Message, state: FSMContext):
    await message.reply("<b>Необходимо дождаться выполнения предыдущей операции!</b>")


@router.message()
async def empty_msg(msg: Message, state: FSMContext):
    await msg.reply(
        "Похоже, что такие сообщения еще не обрабатываются...\n",
    )


@router.callback_query()
async def empty_callback(call: CallbackQuery, state: FSMContext):
    await call.answer("Эта кнопка ничего не даелает 👽")
