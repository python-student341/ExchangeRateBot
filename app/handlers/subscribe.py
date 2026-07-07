from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.common.commands import all_commands
from app.common.limit import limit


router = Router()

@router.message(~Command(*all_commands), limit)
async def subscribe_to_the_bot(message: Message, is_new_user: bool):
    currencies_list = "\n/rub\n/kzt\n/usd"

    if is_new_user:
        await message.answer(
                    f"You have successfully subscribed to exchange rate updates (relative to USD)!\n"
                    f"Now, choose your base currency from this list: {currencies_list}\n\n"
                    f"Then, set your notification preference:\n"
                    f"/on_change — Get notified immediately when the rate shifts\n"
                    f"/by_time — Get updates at a specific time every day\n"
                    f"(Use /set_time to change your notification time)\n\n"
                    f"To check the current rate at any moment, use: /get_exchange_rate"
                )
    else:
        await message.answer(
            f"You can manage your settings at any time:\n\n"
            f"Change currency: {currencies_list}\n\n"
            f"Notification mode:\n"
            f"/on_change — Alert on rate fluctuation\n"
            f"/by_time — Alert on daily schedule\n\n"
            f"Change notification time:\n"
            f"/set_time — Set your preferred daily update time\n\n"
            f"Check exchange rate for your currency right now: /get_exchange_rate"
        )