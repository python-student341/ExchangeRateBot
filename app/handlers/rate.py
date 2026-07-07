from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fast_depends import inject

from app.services.rate import update_currency_service, get_current_exchange_rate_service
from app.database.database import session_dep
from app.common.commands import currency_commands
from app.common.limit import limit


router = Router()

@router.message(Command(*currency_commands), limit)
@inject
async def update_currensy(session: session_dep, message: Message):
    user_choise = message.text.replace("/", "")

    await update_currency_service(session=session, tg_user_id=message.from_user.id, currency=user_choise)
    await message.answer(f"Your currency was updated to: {user_choise}")


@router.message(Command("get_exchange_rate"), limit)
@inject
async def get_current_exchange_rate(session: session_dep, message: Message):
    current_rate, currency = await get_current_exchange_rate_service(session=session, tg_user_id=message.from_user.id)
    await message.answer(f"Current exchange rate for {currency}: {current_rate}")