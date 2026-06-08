import importlib
from typing import Callable

db_provider_mapper={}

'''
Discovers Providers
When a provider name is supplied go and see if a package with that
name exists in data_providers namespace package. If it does load it into memory.
The provider __init__.py is responsible for registering its callable with the db_provider_mapper dictionary.
This is only ever called by db init which is protected by a lock so it is assumed no lock is required here
'''

def get_provider_callable(provider_name: str) -> Callable:
    if provider_name not in db_provider_mapper:
        try:
            importlib.import_module(f"pydbsprocket.data_providers.{provider_name}")
        except ImportError:
            raise RuntimeError(f"Provider {provider_name} Not Implemented")
    provider = db_provider_mapper.get(provider_name, None)
    if provider is None:
        raise RuntimeError(f"Provider {provider_name} Not Implemented")
    return provider