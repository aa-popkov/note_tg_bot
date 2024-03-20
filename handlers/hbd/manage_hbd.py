from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from keyboards.hbd import get_hbd_edit_list_kb, get_hbd_edit_kb, get_hbd_kb
from models import UserHappyBirthday
from models.callback.hbd import HbdCallback, HbdType, HbdDeleteCallback, HbdAction
from utils import states
from utils.kb_data import HbdMenu

router = Router(name=__name__)


@router.message(
    StateFilter(states.MainState.hbd),
    F.text == HbdMenu().mange_hdb,
)
async def get_hbd_edit_msg(msg: Message, user_id: str | None = None):
    if not user_id:
        user_id = str(msg.from_user.id)
    all_hbd_count = await UserHappyBirthday.get_count_by_user(user_id)
    if all_hbd_count == 0:
        await msg.answer(
            text="У тебя еще не заведены Дни рождения 😭\n\n"
            "<i>Воспользуйся клавиатурой внизу</i>",
            reply_markup=get_hbd_kb(),
        )
        return

    all_hbd = await UserHappyBirthday.get_all_hbd_by_user(user_id)
    hb_cb = HbdCallback(
        current_page=0,
        max_page=((all_hbd_count - 1) // 5) + 1,
    )

    await msg.answer(
        text="Выбери день рождение для его удаления",
        reply_markup=get_hbd_edit_list_kb(hb_cb, all_hbd),
    )


@router.callback_query(HbdCallback.filter(F.hbd_type == HbdType.edit_msg))
async def edit_hbd_nav_callback(callback: CallbackQuery):
    cb_data = HbdCallback.unpack(callback.data)
    all_hbd_count = await UserHappyBirthday.get_count_by_user(
        str(callback.from_user.id)
    )
    all_hbd = await UserHappyBirthday.get_all_hbd_by_user(
        str(callback.from_user.id), cb_data.current_page * 5
    )
    cb_data.max_page = ((all_hbd_count - 1) // 5) + 1
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_edit_list_kb(cb_data, all_hbd)
    )


@router.callback_query(HbdDeleteCallback.filter(F.action.func(lambda x: x is None)))
async def edit_hbd_callback(callback: CallbackQuery):
    cb_data = HbdDeleteCallback.unpack(callback.data)
    hbd = await UserHappyBirthday.get_hbd_by_id(cb_data.id)
    if hbd is None:
        return await callback.message.edit_text(
            text="Такой записи не нашлось, возможно она была удалена...",
            reply_markup=None,
        )

    await callback.message.edit_text(
        text=f"🎈 День рождения у:\n"
        f"<b>{hbd.person_name}</b>\n"
        f"📅 Дата:\n"
        f"<b>{hbd.person_birthdate.strftime('%d.%m.%Y')}</b>\n\n",
        reply_markup=get_hbd_edit_kb(cb_data),
    )


@router.callback_query(HbdDeleteCallback.filter(F.action == HbdAction.delete))
async def delete_hbd_callback(callback: CallbackQuery):
    cb_data = HbdDeleteCallback.unpack(callback.data)
    result = await UserHappyBirthday.delete_hbd(cb_data.id)
    if not result:
        await callback.message.edit_text(
            text="Не удалось удалить 😭", reply_markup=None
        )
        await get_hbd_edit_msg(callback.message, str(callback.from_user.id))
        return
    await callback.message.edit_text("Успешно удалено 🥳", reply_markup=None)
    await get_hbd_edit_msg(callback.message, str(callback.from_user.id))
