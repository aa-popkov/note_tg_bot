from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils import states
from keyboards.cats import get_main_cats_kb
from utils.kb_data import MainMenu

router = Router(name=__name__)


@router.message(StateFilter(states.MainState.menu), F.text == MainMenu().cats)
async def cats_menu(msg: Message, state: FSMContext):
    await msg.reply(
        text="Тут можно посмотреть милых(и не только) котиков\n\n"
        "Ты можешь добавить подпись на картинку.\n"
        "Для этого, вместо кнопки на клавиатуре, \n"
        "напиши мне любое сообщение <b>менее 15 символов(включительно)</b>\n\n"
        "Если необходима картинка без текста, то воспользуйся клавиатурой внизу\n"
        "😼",
        reply_markup=get_main_cats_kb(),
    )
    await state.set_state(states.MainState.cats)
