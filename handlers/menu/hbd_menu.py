from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import states
from keyboards.hbd import get_hbd_kb
from utils.kb_data import MainMenu

router = Router(name=__name__)


@router.message(Command("hbd"))
@router.message(StateFilter(states.MainState.menu), F.text == MainMenu().hbd)
async def hbd_menu(msg: Message, state: FSMContext):
    await msg.answer(
        text="<b>Дни рождения</b> твоих\n\n"
             "👨‍👩‍👧‍👦 Родственников\n"
             "🤝 Друзей\n"
             "🕵️‍♂️ Занкомых\n"
             "👽 И кого угодно\n\n"
             "⏰После добавления, я буду автоматически напоминать тебе о них:\n"
             "- за <b>30</b> дней\n"
             "- за <b>14</b> дней\n"
             "- за <b>3</b> дня\n"
             "- за <b>1</b> день\n"
             "- в <b>тот самый день</b>\n\n"
             "<i>Воспользуйся кнопками внизу</i>",
        reply_markup=get_hbd_kb(),
    )
    await state.set_state(states.MainState.hbd)
