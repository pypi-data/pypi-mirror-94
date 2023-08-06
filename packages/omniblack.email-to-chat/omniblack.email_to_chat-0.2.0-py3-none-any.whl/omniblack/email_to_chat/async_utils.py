from asyncio import get_running_loop
from functools import wraps, partial


def run_in_executor(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = get_running_loop()
        return await loop.run_in_executor(
            executor=None,
            func=partial(func, *args, **kwargs),
        )

    wrapper.sync = func
    return wrapper
