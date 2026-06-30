from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.database.database import new_session


async def get_all_users():
    async with new_session() as session:
        result = await session.execute(select(User.tg_user_id))
        return result.scalars().all()


async def create_user(tg_user_id: int, session: AsyncSession):
    stmt = (insert(User).values(tg_user_id=tg_user_id).on_conflict_do_nothing(index_elements=['tg_user_id']))

    await session.execute(stmt)
    await session.commit()