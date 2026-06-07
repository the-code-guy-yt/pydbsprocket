from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod
from .connections import ConnectionConfig


class ProviderBase(ABC):

    @abstractmethod
    def __init__(self, config: ConnectionConfig):
        raise NotImplementedError()

    @abstractmethod
    async def create_pool(self) -> None:
        """Initialize the connection pool."""
        raise NotImplementedError()

    @abstractmethod
    async def close_pool(self) -> None:
        """Close the connection pool."""
        raise NotImplementedError()

    @abstractmethod
    @asynccontextmanager
    async def get_connection(self):
        """Context manager for acquiring database connections."""
        raise NotImplementedError()

    @abstractmethod
    @asynccontextmanager
    async def transaction(self):
        raise NotImplementedError()

    @abstractmethod
    async def call_proc(
            self,
            proc_name: str,
            params: Optional[Dict[str, Any]],
            include_header: bool = False
    ) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    async def get_pool_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics."""
        raise NotImplementedError()

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if database connection is healthy."""
        raise NotImplementedError()


