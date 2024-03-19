from aiogram import Router

from .add_hbd import router as add_hbd_router
from .get_hbd import router as get_hbd_router

router = Router(name=__name__)
router.include_routers(
    add_hbd_router,
    get_hbd_router,
)

__all__ = [
    "router",
]
