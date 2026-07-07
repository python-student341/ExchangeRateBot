from aiogram import Router

from app.handlers.notification import router as notification_router
from app.handlers.rate import router as rate_router
from app.handlers.subscribe import router as subscribe_router


main_router = Router()

main_router.include_router(notification_router)
main_router.include_router(rate_router)
main_router.include_router(subscribe_router)