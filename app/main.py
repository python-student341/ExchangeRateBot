import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.bot_loader import dp, bot
from app.router import main_router
from app.middlewares.user import check_user_registration
from app.services.notification import send_notifications_on_change, send_notifications_by_time


async def on_startup():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notifications_on_change, trigger="interval", minutes=60)
    scheduler.add_job(send_notifications_by_time, trigger="cron", minute="*", second=0)
    scheduler.start()


async def main():
    # 1. Connect middlewares
    dp.message.middleware(check_user_registration)
    
    # 2. Conneсt router
    dp.include_router(main_router)
    
    # 3. Start monitoring in background mode
    dp.startup.register(on_startup)
    
    # 4. Start bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())