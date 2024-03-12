from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.start import get_send_contact_kb
from models import User
from utils import states, config


router = Router(name=__name__)


@router.message(
    StateFilter(states.StartState.start_register),
    F.content_type == ContentType.CONTACT,
)
async def get_contact(msg: Message, state: FSMContext):
    if msg.contact.user_id != msg.from_user.id:
        await msg.answer(
            text="Это чужой контакт!\n" "Попробуй еще раз, хитрая жопа",
            reply_markup=get_send_contact_kb(),
        )
        return

    check_user = await User.get_user_by_tg_id(str(msg.from_user.id))
    if check_user is not None:
        await msg.answer(
            text="Похоже, что ты уже зарегистрирован!\n" "Перевожу в главное меню",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(states.MainState.main)
        return

    user = User(
        tg_id=str(msg.from_user.id),
        phone_num=msg.contact.phone_number,
        username=msg.from_user.username,
    )
    try:
        new_user_id = await User.add_user(user)
    except Exception as e:
        for admin in config.TG_ADMIN_CHAT_ID:
            await msg.bot.send_message(
                chat_id=admin,
                text=f"При регистрации:\n" f"{user}\n" f"Произошла ошибка:\n" f"{e}",
            )
        await msg.answer(
            "😭Не удалось завершить регистрацию...\n"
            "Администраторы в курсе проблемы и уже стараются ее исправить\n"
            "Пожалуйста, попробуйте еще раз через 10 минут"
        )
        return

    await msg.answer(
        text="🥳 Поздравляю!\n"
        "Ты успешно зарегистрирован,\n"
        "Можешь начать работу с ботом",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(states.MainState.main)
