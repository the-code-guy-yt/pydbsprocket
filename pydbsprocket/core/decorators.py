from .provider import get_current_db_provider
from functools import wraps

def db_call_proc(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        db_provider = await get_current_db_provider()
        proc_name, params, include_header, result_key = await func(*args, **kwargs)
        results = await db_provider.call_proc(proc_name, params, include_header)
        return results.get(result_key) if result_key else results
    return wrapper
