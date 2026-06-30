import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.rate import track_rate_changes
from app.utils.bot_loader import dp, bot
from app.handlers.handlers import router
from app.middlewares.user import check_user_registration
from app.services.rate import track_rate_changes


async def on_startup():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(track_rate_changes, trigger="interval", minutes=60)
    scheduler.start()


async def main():
    # 1. Connect middlewares
    dp.message.middleware(check_user_registration)
    
    # 2. Conneсt router
    dp.include_router(router)
    
    # 3. Start monitoring in background mode
    dp.startup.register(on_startup)
    
    # 4. Start bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())