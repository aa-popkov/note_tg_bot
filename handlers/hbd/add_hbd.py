from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from models.callback.calendar import CalendarCallback, CalendarNavigation
from utils import states
from keyboards.hbd import get_hbd_kb, get_hbd_calendar
from utils.kb_data import HbdMenu

router = Router(name=__name__)


@router.message(StateFilter(states.MainState.hbd), F.text == HbdMenu().add_hbd)
async def add_hbd(msg: Message, state: FSMContext):
    await msg.answer(
        text="Введи <b>имя</b> или <b>любой текст</b>\n\n"
        "<i>Длина не должна привышать <b>40 символов</b></i>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(states.HbdState.add_note)


@router.message(StateFilter(states.HbdState.add_note), F.content_type == "text")
async def add_hbd_get_name(msg: Message, state: FSMContext):
    await msg.answer(
        text="Выбери дату",
        reply_markup=get_hbd_calendar(),
    )


@router.message(StateFilter(states.HbdState.add_note), F.content_type != "text")
async def add_hbd_get_non_text(msg: Message, state: FSMContext):
    await msg.reply(
        text="Это не текст!\n\n" "<b>Попробуй еще раз</b>",
    )


@router.callback_query(
    CalendarCallback.filter(F.navigation == CalendarNavigation.back),
    states.HbdState.add_note,
)
async def hbd_back_year_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_calendar(CalendarCallback.unpack(callback.data).year-8)
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(F.navigation == CalendarNavigation.forward),
    states.HbdState.add_note,
)
async def hbd_forward_year_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_calendar(CalendarCallback.unpack(callback.data).year+8)
    )
    await callback.answer("")
