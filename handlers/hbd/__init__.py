from aiogram import Router

from .add_hbd import router as add_hbd_route

router = Router(name=__name__)
router.include_routers(
    add_hbd_route,
)

__all__ = [
    "router",
]
