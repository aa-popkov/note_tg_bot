import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.filters import StateFilter

from utils import states
from utils.kb_data import CatsMenu
from handlers.menu.main_menu import main_menu
from config.config import config
from utils.middlewares import LongTimeMiddleware

router = Router(name=__name__)
router.message.middleware(LongTimeMiddleware())


@router.message(
    StateFilter(states.MainState.cats),
    F.text == CatsMenu().give_cat,
    flags={"long_operation": True},
)
async def get_cats(message: Message, state: FSMContext):
    await state.set_state(states.MainState.wait_operation)
    try:
        connector = aiohttp.TCPConnector(
            verify_ssl=False, use_dns_cache=False
        )  # https://github.com/aio-libs/aiohttp/issues/2522
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                url=f"https://api.thecatapi.com/v1/images/search",
                headers={
                    "Accept": "application/json",
                    "x-api-key": config.CAT_API_KEY,
                },
            ) as resp:
                result = await resp.json()
        cat_img = URLInputFile(
            url=result[0]["url"], filename="some_file_name.jpg", timeout=5
        )
        await message.answer_photo(photo=cat_img)
    except Exception as e:
        await message.answer(
            text="Произошла непредвиденная ошибка 😭\n"
            "Попробуй повторить запрос позже\n\n"
            f'<pre><code class="language-python">{e}</code></pre>'
        )
    finally:
        await state.set_state(states.MainState.cats)


@router.message(StateFilter(states.MainState.cats), F.text == CatsMenu().back_to_menu)
async def back_to_main_menu(message: Message, state: FSMContext):
    await main_menu(message, state)


@router.message(StateFilter(states.MainState.wait_operation))
async def wait_operation(message: Message, state: FSMContext):
    await message.answer("<b>Необходимо дождаться предыдущего котика!</b>")


# ! THIS ROUTE MUST BE LAST IN THIS FILE !
@router.message(
    StateFilter(states.MainState.cats),
    F.content_type == "text",
    flags={"long_operation": True},
)
async def get_cats_with_text(message: Message, state: FSMContext):
    await state.set_state(states.MainState.wait_operation)
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
    finally:
        await state.set_state(states.MainState.cats)
