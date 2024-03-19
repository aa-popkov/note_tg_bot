from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from keyboards.hbd import get_hbd_in_msg_kb
from models import UserHappyBirthday
from models.callback.hbd import HbdCallback, HbdNavigation
from utils import states
from utils.kb_data import HbdMenu
from utils.middlewares import LongTimeMiddleware

router = Router(name=__name__)
router.message.middleware(LongTimeMiddleware())


@router.message(
    StateFilter(states.MainState.hbd),
    F.text == HbdMenu().show_in_msg,
    flags={"long_operation": True},
)
async def get_hbd_in_msg(msg: Message):
    all_hbd_count = await UserHappyBirthday.get_count_by_user(str(msg.from_user.id))
    if all_hbd_count == 0:
        await msg.answer("У тебя еще не заведены Дни рождения 😭\n\n"
                         "<i>Воспользуйся клавиатурой внизу</i>")
        return
    all_hbd = await UserHappyBirthday.get_all_hbd_by_user(str(msg.from_user.id))
    hb_cb = HbdCallback(
        current_page=0,
        max_page=((all_hbd_count - 1) // 5) + 1,
    )
    msg_text = ""
    for hbd in all_hbd:
        msg_text += (
            f"🎈 День рождения у:\n"
            f"<b>{hbd.person_name}</b>\n"
            f"📅 Дата:\n"
            f"<b>{hbd.person_birthdate.strftime('%d.%m.%Y')}</b>\n\n"
        )

    await msg.answer(
        text=msg_text,
        reply_markup=get_hbd_in_msg_kb(hb_cb),
    )


@router.callback_query(HbdCallback.filter())
async def get_hbd_forward_callback(callback: CallbackQuery):
    cb_data = HbdCallback.unpack(callback.data)
    all_hbd_count = await UserHappyBirthday.get_count_by_user(
        str(callback.from_user.id)
    )
    all_hbd = await UserHappyBirthday.get_all_hbd_by_user(
        str(callback.from_user.id), cb_data.current_page * 5
    )
    cb_data.max_page = ((all_hbd_count - 1) // 5) + 1

    msg_text = ""
    for hbd in all_hbd:
        msg_text += (
            f"🎈 День рождения у:\n"
            f"<b>{hbd.person_name}</b>\n"
            f"📅 Дата:\n"
            f"<b>{hbd.person_birthdate.strftime('%d.%m.%Y')}</b>\n\n"
        )

    await callback.message.edit_text(
        text=msg_text,
        reply_markup=get_hbd_in_msg_kb(cb_data)
    )
