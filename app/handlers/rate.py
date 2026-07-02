from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fast_depends import inject

from app.services.rate import update_currency_service, get_current_exchange_rate_service
from app.database.database import session_dep
from app.common.commands import currency_commands, all_commands


router = Router()


@router.message(~Command(*all_commands))
async def subscribe_to_the_bot(message: Message, is_new_user: bool):
    currencies_list = "\n/rub\n/kzt\n/usd"

    if is_new_user:
        await message.answer(
                    f"You have successfully subscribed to exchange rate updates (relative to USD)!\n"
                    f"Now, choose your base currency from this list: {currencies_list}\n\n"
                    f"Then, set your notification preference:\n"
                    f"/on_change — Get notified immediately when the rate shifts\n"
                    f"/by_time — Get updates at a specific time every day\n\n"
                    f"To check the current rate at any moment, use: /get_exchange_rate"
                )
    else:
        await message.answer(
            f"You can manage your settings at any time:\n\n"
            f"Change currency: {currencies_list}\n\n"
            f"Notification mode:\n"
            f"/on_change — Alert on rate fluctuation\n"
            f"/by_time — Alert on daily schedule\n\n"
            f"Check exchange rate for your currency right now: /get_exchange_rate"
        )


@router.message(Command(*currency_commands))
@inject
async def update_currensy(session: session_dep, message: Message):
    user_choise = message.text.replace("/", "")

    await update_currency_service(session=session, tg_user_id=message.from_user.id, currency=user_choise)
    await message.answer(f"Your currency was updated to: {user_choise}")


@router.message(Command("get_exchange_rate"))
@inject
async def get_current_exchange_rate(session: session_dep, message: Message):
    current_rate, currency = await get_current_exchange_rate_service(session=session, tg_user_id=message.from_user.id)
    await message.answer(f"Current exchange rate for {currency}: {current_rate}")