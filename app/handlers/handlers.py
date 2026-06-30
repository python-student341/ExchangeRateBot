from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fast_depends import inject

from app.services.rate import update_currency
from app.database.database import session_dep


router = Router()

currency_commands = ["rub", "kzt", "usd"]


@router.message(~Command(*currency_commands))
async def subscribe_to_the_bot(message: Message, is_new_user: bool):
    currencies_list = "\n/rub\n/kzt\n/usd"

    if is_new_user:
        await message.answer(f"You have successfully subscribed to exchange rate updates!\nNow, choose your currency from this list: {currencies_list}")
    else:
        await message.answer(f"You can change your currency at any time of this list: {currencies_list}")


@router.message(Command(*currency_commands))
@inject
async def choose_currensy(message: Message, session: session_dep):
    user_choise = message.text.replace("/", "")

    await update_currency(session=session, tg_user_id=message.from_user.id, currency=user_choise)
    await message.answer(f"You choose {user_choise} currency")