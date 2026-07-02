from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.user import User, NotificationMode
from app.utils.bot_loader import bot
from app.helpers.notification import get_users_by_notification_mode
from app.helpers.rate import fetch_all_rates


async def update_notification_mode_service(session: AsyncSession, tg_user_id: int, notification_mode: str):
    query = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    current_user = query.scalar_one_or_none()

    current_user.notification_mode = NotificationMode(notification_mode)

    await session.commit()
    await session.refresh(current_user)


async def send_notifications_by_time():
    rates = await fetch_all_rates()
    users = await get_users_by_notification_mode(NotificationMode.by_time)

    for tg_user_id, user_currency in users:
        currency = user_currency.value
        current_rate = rates[currency]
            
        await bot.send_message(
            chat_id=tg_user_id,
            text=f"Hello! Exchange rate for your currency now: {current_rate}"
        )


last_rates = {
    "rub": None,
    "kzt": None,
    "usd": None
}

async def send_notifications_on_change():
    global last_rates

    new_rates = await fetch_all_rates()
    users = await get_users_by_notification_mode(NotificationMode.on_change)

    for tg_user_id, user_currency in users:
        currency = user_currency.value
                
        old_rate = last_rates[currency]
        current_rate = new_rates[currency]

        if current_rate != old_rate and current_rate is not None:
            await bot.send_message(
                chat_id=tg_user_id,
                text=f"Exchange rate for {currency} was changed! Latest rate: {current_rate}"
            )

    last_rates = new_rates