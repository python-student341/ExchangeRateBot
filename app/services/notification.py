from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime

from app.models.user import User, NotificationMode
from app.core.bot_loader import bot
from app.helpers.rate import fetch_all_rates
from app.database.database import new_session


async def update_notification_mode_service(session: AsyncSession, tg_user_id: int, notification_mode: str):
    query = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    current_user = query.scalar_one_or_none()

    current_user.notification_mode = NotificationMode(notification_mode)

    await session.commit()
    await session.refresh(current_user)


async def update_notification_time_service(session: AsyncSession, current_user: User, new_notification_time: str):
    current_user.notification_time = new_notification_time

    await session.commit()
    await session.refresh(current_user)



async def send_notifications_by_time():
    rates = await fetch_all_rates()

    current_time = datetime.datetime.now().strftime("%H:%M")

    async with new_session() as session:
        query = await session.execute(select(User).where(User.notification_mode == NotificationMode.by_time, User.notification_time == current_time))
        users = query.scalars().all()

    for current_user in users:
        currency = current_user.currency.value
        current_rate = rates[currency]
            
        await bot.send_message(
            chat_id=current_user.tg_user_id,
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
    async with new_session() as session:
        query = await session.execute(select(User.tg_user_id, User.currency).where(User.notification_mode == NotificationMode.on_change))
        users = query.all()

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