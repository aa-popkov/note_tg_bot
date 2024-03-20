from typing import List

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from keyboards.hbd import get_hbd_in_msg_kb
from models import UserHappyBirthday
from models.callback.hbd import HbdCallback, HbdNavigation, HbdType
from utils import states
from utils.kb_data import HbdMenu
from utils.middlewares import LongTimeMiddleware

from utils.templates import create_render_page

router = Router(name=__name__)
router.message.middleware(LongTimeMiddleware())


@router.message(
    StateFilter(states.MainState.hbd),
    F.text == HbdMenu().show_in_msg,
    flags={"long_operation": True},
)
async def get_hbd_in_msg(msg: Message, state: FSMContext):
    await state.set_state(states.MainState.wait_operation)
    try:
        all_hbd_count = await UserHappyBirthday.get_count_by_user(str(msg.from_user.id))
        if all_hbd_count == 0:
            await msg.answer(
                "У тебя еще не заведены Дни рождения 😭\n\n"
                "<i>Воспользуйся клавиатурой внизу</i>"
            )
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
    finally:
        await state.set_state(states.MainState.hbd)


@router.callback_query(HbdCallback.filter(F.hbd_type == HbdType.show_in_msg))
async def get_hbd_nav_callback(callback: CallbackQuery):
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
        text=msg_text, reply_markup=get_hbd_in_msg_kb(cb_data)
    )


@router.message(
    StateFilter(states.MainState.hbd),
    F.text == HbdMenu().show_html,
    flags={"long_operation": True},
)
async def get_hbd_in_file(msg: Message, state: FSMContext):
    await state.set_state(states.MainState.wait_operation)
    try:
        all_hbd_count = await UserHappyBirthday.get_count_by_user(str(msg.from_user.id))
        if all_hbd_count == 0:
            await msg.answer(
                "У тебя еще не заведены Дни рождения 😭\n\n"
                "<i>Воспользуйся клавиатурой внизу</i>"
            )
            return
        all_hbd: List[UserHappyBirthday] = []
        for page in range(0, all_hbd_count, 5):
            hbds: List[UserHappyBirthday] = await UserHappyBirthday.get_all_hbd_by_user(
                str(msg.from_user.id), page
            )
            all_hbd += hbds

        hbd_html: str = create_render_page("hbd", all_hbd)
        hbd_bytes = hbd_html.encode("utf-8")
        hbd_file = BufferedInputFile(file=hbd_bytes, filename="hbd.html")

        await msg.reply_document(
            document=hbd_file,
        )
    finally:
        await state.set_state(states.MainState.hbd)
