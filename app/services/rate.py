from httpx import AsyncClient
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import url
from app.utils.bot_loader import bot
from app.database.database import new_session
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


last_rates = {
    "rub": None,
    "kzt": None,
    "usd": None
}

async def track_rate_changes():
    global last_rates

    rub_rate, kzt_rate, usd_rate = await asyncio.gather(
            get_exchange_rate(url, "rub"),
            get_exchange_rate(url, "kzt"),
            get_exchange_rate(url, "usd")
        )

    new_rates = {
        "rub": rub_rate,
        "kzt": kzt_rate,
        "usd": usd_rate
    }
    
    async with new_session() as session:
        query = await session.execute(select(User.tg_user_id, User.currency))
        all_users = query.all()

    for tg_user_id, user_currency in all_users:
        #Get currency from new_rates
        if hasattr(user_currency, 'value'):
            currency = user_currency.value
        else:
            currency = user_currency
                
        old_rate = last_rates[currency]
        current_rate = new_rates[currency]

        if current_rate != old_rate and current_rate is not None:
            await bot.send_message(
                chat_id=tg_user_id,
                text=f"Exchange rate for {currency} was changed! Latest rate: {current_rate}"
            )

    last_rates = new_rates


#Will be used in the next commit
#async def get_current_exchange_rate_service(current_currency: str = None):
#    if not current_currency:
#        current_currency = currency

#    rate = await get_exchange_rate(url, current_currency)
#    return rate


async def update_currency(currency: str, tg_user_id: int, session: AsyncSession):
    query = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    current_user = query.scalar_one_or_none()

    if current_user:
        current_user.currency = Currency(currency)

        await session.commit()
        await session.refresh(current_user)