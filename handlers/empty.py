from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

router = Router(name=__name__)


@router.message()
async def empty_msg(msg: Message, state: FSMContext):
    await msg.reply(
        "Похоже, что такие сообщения еще не обрабатываются...\n",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.callback_query()
async def empty_callback(call: CallbackQuery, state: FSMContext):
    await call.answer("Эта кнопка ничего не даелает 👽")
