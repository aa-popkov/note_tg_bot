from aiogram import Router
from .main_menu import router as main_menu_router
from .notes_menu import router as route_menu_router
from .cats_menu import router as cats_menu_router

router = Router(name=__name__)
router.include_routers(
    main_menu_router,
    route_menu_router,
    cats_menu_router,
)

__all__ = [
    "router",
]
