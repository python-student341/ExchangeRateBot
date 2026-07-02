import asyncio

from app.services.rate import get_exchange_rate
from app.config import url


async def fetch_all_rates():
    rub_rate, kzt_rate, usd_rate = await asyncio.gather(
        get_exchange_rate(url, "rub"),
        get_exchange_rate(url, "kzt"),
        get_exchange_rate(url, "usd")
    )

    return {
        "rub": rub_rate,
        "kzt": kzt_rate,
        "usd": usd_rate
    }