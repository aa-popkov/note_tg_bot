from aiogram import Router

from .empty import router as empty_router
from .start import router as start_router
from .menu import router as menu_router
from .notes import router as notes_router
from .cats import router as cats_router
from .hbd import router as hbd_route

router = Router(name=__name__)
router.include_routers(
    start_router,
    menu_router,
    notes_router,
    cats_router,
    hbd_route,
)

# ! Must be last
router.include_router(empty_router)

__all__ = [
    "router",
]
