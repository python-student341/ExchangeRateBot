from app.helpers.rate_limiter import rate_limiter_factory

limit = rate_limiter_factory("action", 5, 10)