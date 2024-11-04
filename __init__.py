__all__ = ('router',)
from aiogram import Router
from handlers_and_keyboards import router as h_and_k_router
router = Router()
router.include_routers(h_and_k_router)
