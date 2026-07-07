from redis.asyncio import Redis
import random
from time import time


class RateLimiter:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_limited(self, key_suffix: str, action_name: str, max_requests: int, window_seconds: int) -> bool:
        key = f"rate_limiter:{action_name}:{key_suffix}"
        current_ms = time() * 1000
        window_start_ms = current_ms - window_seconds * 1000
        current_request = f"{current_ms}-{random.randint(0, 100_000)}"

        async with self._redis.pipeline() as pipeline:
            pipeline.zremrangebyscore(key, 0, window_start_ms)
            pipeline.zcard(key)
            pipeline.zadd(key, {current_request: current_ms})

            pipeline.expire(key, window_seconds)
            
            result = await pipeline.execute()

        _, current_count, _, _ = result

        if current_count >= max_requests:
            return True

        return False