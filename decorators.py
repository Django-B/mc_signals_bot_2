import aiosqlite, asyncio
from functools import wraps

async def retry_yield(func):
    retry_delay = 5
    max_retries = 5
    async def wrapper(*args, **kwargs):
        for attempt in range(1, max_retries+1):
            try:
                async for game in func(*args, **kwargs):
                    yield game
                break
            except aiosqlite.Error as e:
                if e.args == "database is locked":
                    print(f"Database is locked. Waiting for {retry_delay} seconds... (Attempt {attempt+1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                else:
                    raise
        else:
            print("Max retries exceeded. Giving up.")
            raise
    return wrapper

async def retry(func):
    retry_delay = 5
    max_retries = 5
    async def wrapper(*args, **kwargs):
        for attempt in range(1, max_retries+1):
            try:
                return await func(*args, **kwargs)
            except aiosqlite.Error as e:
                if e.args == "database is locked":
                    print(f"Database is locked. Waiting for {retry_delay} seconds... (Attempt {attempt+1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                else:
                    raise
        else:
            print("Max retries exceeded. Giving up.")
            raise
    return wrapper

def retry_on_locked_database_yield(max_retries=5, retry_delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    async for result in func(*args, **kwargs):
                        yield result
                    break
                except aiosqlite.Error as e:
                    if e.args == "database is locked":
                        print(f"Database is locked. Waiting for {retry_delay} seconds... (Attempt {attempt+1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                    else:
                        raise
            else:
                print("Max retries exceeded. Giving up.")
                raise
        return wrapper
    return decorator

def retry_on_locked_database(max_retries=5, retry_delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except aiosqlite.Error as e:
                    if e.args == "database is locked":
                        print(f"Database is locked. Waiting for {retry_delay} seconds... (Attempt {attempt+1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                    else:
                        raise
            else:
                print("Max retries exceeded. Giving up.")
                raise
        return wrapper
    return decorator
