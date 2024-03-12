from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.filters import StateFilter

from utils import states
from utils.kb_data import CatsMenu
from handlers.menu.main_menu import main_menu

router = Router(name=__name__)


# TODO: Добавить обработку долгих сообщений
@router.message(StateFilter(states.MainState.cats), F.text == CatsMenu().give_cat)
async def get_cats(message: Message, state: FSMContext):
    try:
        cat_img = URLInputFile(
            url="https://cataas.com/cat", filename="some_file_name.jpg", timeout=5
        )
        await message.answer_photo(photo=cat_img)
    except Exception as e:
        await message.answer(
            text="Произошла непредвиденная ошибка 😭\n"
            "Попробуй повторить запрос позже\n\n"
            f'<pre><code class="language-python">{e}</code></pre>'
        )


@router.message(StateFilter(states.MainState.cats), F.text == CatsMenu().back_to_menu)
async def back_to_main_menu(message: Message, state: FSMContext):
    await main_menu(message, state)


# ! THIS ROUTE MUST BE LAST IN THIS FILE !
@router.message(StateFilter(states.MainState.cats), F.content_type == "text")
async def get_cats_with_text(message: Message, state: FSMContext):
    if len(message.text.strip()) > 15:
        await message.answer(
            text="Длина текста должна быть <b>меньше 15 символов!</b>\n"
            "Попробуй еще раз 😼",
        )
        return

    try:
        cat_img = URLInputFile(
            url=f"https://cataas.com/cat/says/{message.text.strip()}?fontColor=aquamarine",
            filename="some_file_name.jpg",
            timeout=5,
        )
        await message.answer_photo(photo=cat_img)
    except Exception as e:
        await message.answer(
            text="Произошла непредвиденная ошибка 😭\n"
            "Попробуй повторить запрос позже\n\n"
            f'<pre><code class="language-python">{e}</code></pre>'
        )
