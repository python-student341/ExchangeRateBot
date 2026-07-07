from aiogram import Router, F
from aiogram.types import Message, ForceReply
from aiogram.filters import Command
from fast_depends import inject, Depends
import datetime

from app.services.notification import update_notification_mode_service, update_notification_time_service
from app.common.commands import notification_mode_commands, notification_time_commands
from app.database.database import session_dep
from app.models.user import User
from app.dependencies.notification import check_notification_mode
from app.common.limit import limit


router = Router()

@router.message(Command(*notification_mode_commands), limit)
@inject
async def update_notification_mode(session: session_dep, message: Message):
    user_choise = message.text.replace("/", "")
    
    await update_notification_mode_service(session=session, tg_user_id=message.from_user.id, notification_mode=user_choise)
    await message.answer(f"Your notification mode was updated to: {user_choise}")
    if user_choise == "by_time":
        await message.answer("You can also set the time for notification with this command: /set_time")


@router.message(Command(*notification_time_commands), limit)
async def cmd_set_time(message: Message):
    await message.answer(
            "Enter the time at which you want to receive a notification (like: 09:30).",
            parse_mode="Markdown",
            reply_markup=ForceReply(selective=True)
        )

@router.message(F.reply_to_message.text.contains("Enter the time at which you want to receive a notification (like: 09:30)."), limit)
@inject
async def update_notification_time(session: session_dep, message: Message, current_user: User = Depends(check_notification_mode)):
    time = message.text.strip()

    try:
        datetime.datetime.strptime(time, "%H:%M")
    except ValueError:
        await message.answer("Invalid format. Try again! Click /set_time and enter time like this: 09:30")
        return

    await update_notification_time_service(session=session, current_user=current_user, new_notification_time=time)
    await message.answer(f"Okay, now you will receive a notification about your currency rate every day at this time: {time}")