import importlib
from typing import Callable

_pending_provider = None
_db_provider_registry={}

'''
Discovers Providers
When a provider name is supplied go and see if a package with that
name exists in data_providers namespace package. If it does load it into memory.
The provider __init__.py is responsible for registering its callable with the db_provider_mapper dictionary.
This is only ever called by db init which is protected by a lock so it is assumed no lock is required here
'''

def _raise_provider_not_implemented(provider_name):
    global _pending_provider
    _pending_provider = None
    raise RuntimeError(f"Provider {provider_name} Not Implemented")

def register_provider(provider_class: Callable):
    global _db_provider_registry
    global _pending_provider
    _db_provider_registry[_pending_provider] = provider_class
    _pending_provider = None

def get_provider_callable(provider_name: str) -> Callable:
    global _pending_provider

    if provider_name not in _db_provider_registry:
        try:
            _pending_provider = provider_name
            importlib.import_module(f"pydbsprocket.data_providers.{provider_name}")
        except ImportError:
            _raise_provider_not_implemented(provider_name)
    provider = _db_provider_registry.get(provider_name, None)
    if provider is None:
        _raise_provider_not_implemented(provider_name)
    return provider