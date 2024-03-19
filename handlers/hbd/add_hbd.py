import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from models import UserHappyBirthday
from models.callback.calendar import CalendarCallback, CalendarNavigation, CalendarObj
from utils import states
from keyboards.hbd import (
    get_hbd_kb,
    get_hbd_year_calendar,
    get_hbd_month_calendar,
    get_hbd_day_calendar,
)
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
    if len(msg.text.strip()) > 40:
        await msg.answer("<b>Текст не должен превышать 40 символов!</b>\n"
                         "<i>Попробуй еще раз</i>")
        return
    await state.set_data({"hbd_name": msg.text.strip()})
    await msg.answer(
        text="Выбери дату",
        reply_markup=get_hbd_year_calendar(),
    )


@router.message(StateFilter(states.HbdState.add_note), F.content_type != "text")
async def add_hbd_get_non_text(msg: Message):
    await msg.reply(
        text="Это не текст!\n\n" "<b>Попробуй еще раз</b>",
    )


@router.callback_query(
    CalendarCallback.filter(
        (F.navigation == CalendarNavigation.back) & (F.obj == CalendarObj.year)
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_back_year_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_year_calendar(
            CalendarCallback.unpack(callback.data).year - 8
        )
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.navigation == CalendarNavigation.forward) & (F.obj == CalendarObj.year)
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_forward_year_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_year_calendar(
            CalendarCallback.unpack(callback.data).year + 8
        )
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(F.obj == CalendarObj.year),
    StateFilter(states.HbdState.add_note),
)
async def hbd_year_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_month_calendar(CalendarCallback.unpack(callback.data))
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.month) & (F.navigation == CalendarNavigation.forward)
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_month_forward_callback(callback: CallbackQuery):
    cb_data = CalendarCallback.unpack(callback.data)
    cb_data.year += 1
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_month_calendar(cb_data)
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.month) & (F.navigation == CalendarNavigation.back)
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_month_back_callback(callback: CallbackQuery):
    cb_data = CalendarCallback.unpack(callback.data)
    cb_data.year -= 1
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_month_calendar(cb_data)
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.month) & (F.month.func(lambda x: x is None))
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_month_year_callback(callback: CallbackQuery):
    cb_data = CalendarCallback.unpack(callback.data)
    await callback.message.edit_reply_markup(
        reply_markup=get_hbd_year_calendar(cb_data.year)
    )
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.month) & (F.month.func(lambda x: x is not None))
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_month_callback(callback: CallbackQuery):
    cb_data = CalendarCallback.unpack(callback.data)
    await callback.message.edit_reply_markup(reply_markup=get_hbd_day_calendar(cb_data))
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.day) & (F.navigation == CalendarNavigation.back)
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_month_back_callback(callback: CallbackQuery):
    cb_data = CalendarCallback.unpack(callback.data)
    cb_data.month = cb_data.month - 1 if cb_data.month > 0 else 11
    cb_data.year = cb_data.year if cb_data.month > 0 else cb_data.year - 1
    await callback.message.edit_reply_markup(reply_markup=get_hbd_day_calendar(cb_data))
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.day) & (F.navigation == CalendarNavigation.forward)
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_month_forward_callback(callback: CallbackQuery):
    cb_data = CalendarCallback.unpack(callback.data)
    cb_data.month = cb_data.month + 1 if cb_data.month < 11 else 0
    cb_data.year = cb_data.year if cb_data.month < 11 else cb_data.year + 1
    await callback.message.edit_reply_markup(reply_markup=get_hbd_day_calendar(cb_data))
    await callback.answer("")


@router.callback_query(
    CalendarCallback.filter(
        (F.obj == CalendarObj.day) & (F.day.func(lambda x: x is not None))
    ),
    StateFilter(states.HbdState.add_note),
)
async def hbd_select_date_callback(callback: CallbackQuery, state: FSMContext):
    cb_data = CalendarCallback.unpack(callback.data)
    hbd_date = datetime.date(cb_data.year, cb_data.month+1, cb_data.day)
    hbd_name = await state.get_data()
    hbd_id = await UserHappyBirthday.add_hbd(UserHappyBirthday(
        person_name=hbd_name["hbd_name"],
        person_birthdate=hbd_date,
        user_id=str(callback.from_user.id)
    ))

    await callback.message.edit_text(
        text=f"День рождения успешно добавлен:\n\n"
             f"Имя: {hbd_name['hbd_name']}\n"
             f"Дата: {hbd_date.strftime('%d.%m.%Y')}\n"
             f"ID: {hbd_id}",
        reply_markup=None,
    )
    await state.set_state(states.MainState.hbd)
    await state.set_data({})
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text="Перевожу в меню Дней рождений",
        reply_markup=get_hbd_kb()
    )
