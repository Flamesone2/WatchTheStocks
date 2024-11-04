__all__ = ('router',)


from .handlers import router as handlers_router
from .keyboards import router as keyboards_router
from aiogram import Router

router = Router(name=__name__)

router.include_routers(handlers_router, keyboards_router)



