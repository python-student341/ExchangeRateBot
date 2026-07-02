from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.types import Message

from app.models.user import User, NotificationMode


async def check_notification_mode(session: AsyncSession, message: Message):
    query = await session.execute(select(User).where(User.tg_user_id == message.from_user.id))
    current_user = query.scalar_one_or_none()

    if current_user.notification_mode == NotificationMode.on_change:
        await message.answer(
                            "You cannot set a notification time because your current mode is not 'by_time'.\n"
                            "Please switch your mode using /by_time first!"
                        )
        raise ValueError()
        
    return current_user