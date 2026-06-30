from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fast_depends import inject

from app.services.rate import update_currency, get_current_exchange_rate_service
from app.database.database import session_dep
from app.models.user import Currency


router = Router()

currency_commands = ["rub", "kzt", "usd"]
all_commands = [*currency_commands, "get_exchange_rate"]


@router.message(~Command(*all_commands))
async def subscribe_to_the_bot(message: Message, is_new_user: bool):
    currencies_list = "\n/rub\n/kzt\n/usd"

    if is_new_user:
        await message.answer(
                    f"You have successfully subscribed to exchange rate updates (relative to USD)!\n"
                    f"Now, choose your currency from this list: {currencies_list}\n"
                    f"Also, if you want to see the exchange rate of your currency now, use this command:\n/get_exchange_rate"
                )
    else:
        await message.answer(
            f"You can change your currency at any time from this list: {currencies_list}\n"
            f"Or see the exchange rate for your currency right now with this command:\n/get_exchange_rate"
        )


@router.message(Command(*currency_commands))
@inject
async def choose_currensy(session: session_dep, message: Message):
    user_choise = message.text.replace("/", "")

    await update_currency(session=session, tg_user_id=message.from_user.id, currency=user_choise)
    await message.answer(f"You choose {user_choise} currency")


@router.message(Command("get_exchange_rate"))
@inject
async def get_current_exchange_rate(session: session_dep, message: Message):
    current_rate, currency = await get_current_exchange_rate_service(session=session, tg_user_id=message.from_user.id)
    await message.answer(f"Current exchange rate for {currency}: {current_rate}")