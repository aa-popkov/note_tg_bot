from aiogram import Router

from .get_cats import router as get_cats_router

router = Router(name=__name__)
router.include_routers(
    get_cats_router,
)

__all__ = [
    "router",
]
