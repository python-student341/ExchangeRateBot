from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from fast_depends import inject

from app.services.notification import update_notification_mode_service
from app.common.commands import notification_mode_commands
from app.database.database import session_dep


router = Router()

@router.message(Command(*notification_mode_commands))
@inject
async def update_notification_mode(session: session_dep, message: Message):
    user_choise = message.text.replace("/", "")
    
    await update_notification_mode_service(session=session, tg_user_id=message.from_user.id, notification_mode=user_choise)
    await message.answer(f"Your notification mode was updated to: {user_choise}")