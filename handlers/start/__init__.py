from aiogram import Router

from .start import router as start_router
from .registration import router as registration_router
from .contact import router as contact_router

router = Router(name=__name__)
router.include_routers(
    start_router,
    registration_router,
    contact_router,
)

__all__ = ["router"]
