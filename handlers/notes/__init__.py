from aiogram import Router
from .create_note import router as create_note_router
from .get_notes import router as get_notes_router
from .note_action import router as action_note_router

router = Router(name=__name__)
router.include_routers(
    create_note_router,
    get_notes_router,
    action_note_router,
)

__all__ = [
    "router",
]
