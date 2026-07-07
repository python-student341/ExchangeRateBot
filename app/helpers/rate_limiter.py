from aiogram.types import Message

from app.utils.rate_limiter import RateLimiter
from app.database.redis_database import redis

rate_limiter = RateLimiter(redis)

def rate_limiter_factory(action_name: str, max_requests: int, window_seconds: int):
    async def dependency(message: Message):

        limited = await rate_limiter.is_limited(
            key_suffix=str(message.from_user.id),
            action_name=action_name,
            max_requests=max_requests,
            window_seconds=window_seconds
        )

        if limited:
            await message.answer("Too many requests")
            return False
        
        return True

    return dependency