import inspect
import os
import pickle
from functools import wraps

from redis.asyncio import Redis

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=0,
    password=os.getenv("REDIS_PASSWORD"),
)


def cache_response(ttl: int = 60, ignore_keys: list = None):
    if ignore_keys is None:
        ignore_keys = []

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get params names
            sig = inspect.signature(func)
            params = sig.parameters.keys()

            # Delete ignore params
            filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ignore_keys}
            filtered_args = tuple(
                arg for i, arg in enumerate(args) if list(params)[i] not in ignore_keys
            )

            cache_key = f"{func.__name__}:{filtered_args}:{filtered_kwargs}"

            cached_data = await redis.get(cache_key)
            if cached_data:
                return pickle.loads(cached_data)

            result = await func(*args, **kwargs)

            await redis.set(cache_key, pickle.dumps(result), ex=ttl)
            return result

        return wrapper

    return decorator
