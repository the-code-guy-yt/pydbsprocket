import asyncio
from .provider_mapping import get_provider_callable
from .connections import ConnectionConfig

__active_db_provider = None
__dp_creation_lock = asyncio.Lock()


async def init_db_provider(provider_name: str, connection_config: ConnectionConfig):
    global __active_db_provider

    if not __active_db_provider:
        async with __dp_creation_lock:
            if not __active_db_provider:
                f_provider = get_provider_callable(provider_name)
                __active_db_provider = f_provider(connection_config)
          
    return __active_db_provider

async def get_current_db_provider():
    #Create and return a new singleton database connection
    global __active_db_provider
    
    if __active_db_provider:
        return __active_db_provider
    
    raise RuntimeError('Database Must be Initialized Before Use')
    