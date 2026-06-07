#Provider Mapping Dicts
import importlib
from typing import Callable

db_provider_mapper={}

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