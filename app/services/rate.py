from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import url
from app.models.user import User, Currency


async def get_exchange_rate(url: str, currency: str):

    async with AsyncClient() as client:
        query_params = {
            'text': currency
        }
        
        resp = await client.get(url, params=query_params)

        if resp.status_code != 200:
            print('The request failed with an error', resp.text) 
            return None

        all_data = resp.json()
        target_currency = all_data["usd"][currency]

        return target_currency


async def get_current_exchange_rate_service(session: AsyncSession, tg_user_id: int):
    query = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    current_user = query.scalar_one_or_none()

    currency = current_user.currency.value

    current_rate = await get_exchange_rate(url, currency)
    if not current_rate:
        return None

    return current_rate, currency


async def update_currency_service(session: AsyncSession, currency: str, tg_user_id: int):
    query = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    current_user = query.scalar_one_or_none()

    current_user.currency = Currency(currency)

    await session.commit()
    await session.refresh(current_user)