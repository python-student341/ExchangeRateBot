from sqlalchemy import select

from app.models.user import User, NotificationMode
from app.database.database import new_session


async def get_users_by_notification_mode(mode: NotificationMode):
    async with new_session() as session:
        query = await session.execute(select(User.tg_user_id, User.currency).where(User.notification_mode == mode))
        return query.all()