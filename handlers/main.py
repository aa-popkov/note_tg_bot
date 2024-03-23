from typing import List

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder

from utils import states
from utils.middlewares import GetMediaGroupMiddleware

router = Router(name=__name__)
router.message.middleware(GetMediaGroupMiddleware())


@router.message(StateFilter(states.MainState.wait_operation))
async def wait_operation(message: Message, state: FSMContext):
    await message.reply("<b>Необходимо дождаться выполнения предыдущей операции!</b>")


@router.message(
    (F.content_type == ContentType.PHOTO) & (F.media_group_id is not None),
    flags={"get_media_group": True},
)
async def test_media_group(message: Message, album: List[Message]):
    media_group = MediaGroupBuilder(caption="Album")
    for photo in album:
        media_group.add_photo(media=photo.photo[-1].file_id, type="photo")
    await message.answer_media_group(media=media_group.build())


@router.message()
async def empty_msg(msg: Message, state: FSMContext):
    await msg.reply(
        "Похоже, что такие сообщения еще не обрабатываются...\n",
    )


@router.callback_query()
async def empty_callback(call: CallbackQuery, state: FSMContext):
    await call.answer("Эта кнопка ничего не даелает 👽")
