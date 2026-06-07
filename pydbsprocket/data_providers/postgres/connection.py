import asyncpg
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from pydbsprocket.core.connections import ConnectionConfig
from pydbsprocket.core.base import ProviderBase
from pydbsprocket.core.db_types import Param, OutputParameter, InputCollectionParameter, DataType
from pydbsprocket.core.exceptions import *

class PostgresSQLProvider(ProviderBase):
    
    def __init__(self, config: ConnectionConfig):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None
    
    async def create_pool(self) -> None:
        """Initialize the connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                min_size=self.config.min_pool_size,
                max_size=self.config.max_pool_size,
                command_timeout=self.config.command_timeout,
                max_inactive_connection_lifetime=self.config.max_inactive_connection_lifetime,
                server_settings={
                    'search_path': self.config.schema
                }
            )
        except Exception as e:
            raise ConnectionPoolError(
                f"Failed to create connection pool to {self.config.host}:{self.config.port}/{self.config.database}: {str(e)}"
            ) from e
    
    async def close_pool(self) -> None:
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
    
    async def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            raise HealthCheckError(f"Database health check failed: {e}") from e
    
    @asynccontextmanager
    async def get_connection(self):
        """Context manager for acquiring database connections."""
        if not self.pool:
            raise ConnectionPoolError("Database pool not initialized. Call create_pool() first.")
        
        try:
            async with self.pool.acquire() as conn:
                yield conn
        except Exception as e:
            raise ConnectionError(f"Database connection failed: {e}") from e
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        async with self.get_connection() as conn:
            async with conn.transaction():
                yield conn
    
    @staticmethod
    def _render_param(index, param: Any)-> str:
        retval :str = f'${index+1}'
        if isinstance(param, InputCollectionParameter):
            retval += f'::{param.type}[]'
        else:
            if isinstance(param, OutputParameter): #and not param.type == DataType.CURSOR:
                retval += f'::{param.type.value}'

        return retval
    
    @staticmethod
    def _build_proc_command(
            proc_name: str,
            params: Optional[Dict[str, Any]] = None
    ):
        param_markers = ''
        param_vals = []
        
        if params:
            param_markers = ', '.join(
                PostgresSQLProvider._render_param(idx, param)
                for idx, param in enumerate(params.values())
            )
            param_vals = [
                param.value if isinstance(param, Param) else param
                for param in params.values()
            ]
        
        return f'CALL {proc_name}({param_markers})', *param_vals
    
    @staticmethod
    async def _fetch_refcursor_all(
            conn: asyncpg.Connection,
            cursor_name: str,
            chunk: int = 1000,
            include_header: bool = False
    ) -> list:
        """Fetch all rows from a refcursor, return as list of tuples or dicts."""
        rows = []
        header = None
        while True:
            batch = await conn.fetch(f'FETCH FORWARD {chunk} IN "{cursor_name}"')
            if not batch:
                break
            if include_header and header is None:
                header = tuple(batch[0].keys())
                
            rows.extend(tuple(r) for r in batch)
        await conn.execute(f'CLOSE "{cursor_name}"')
        
        if header is not None:
            rows = [header] + rows
            
        return rows
    
    async def fetch_parameter_values(
            self,
            conn,
            out: dict[str, Any],
            params: dict[str, Any],
            include_header: bool = False
    ) -> dict[str, Any]:
        for key, out_val in out.items():
            spec = params.get(key)
            if (
                    isinstance(spec, OutputParameter)
                    and spec.type == DataType.CURSOR
                    and isinstance(out_val, str)
               ):
                params[key] = await self._fetch_refcursor_all(
                    conn,
                    out_val,
                    chunk=2000,
                    include_header=include_header
                )
            else:
                params[key] = out_val
                
        return params
    
    async def call_proc(
        self,
        proc_name: str,
        params: Optional[Dict[str, Any]],
        include_header: bool = False
    ) -> Optional[Dict[str, Any]]:
        
        cmd = self._build_proc_command(proc_name=proc_name, params=params)
        try:
            async with self.transaction() as conn:
                results = await conn.fetchrow(*cmd)
                if results is not None:
                    results = await self.fetch_parameter_values(
                        conn,
                        dict(results),
                        params,
                        include_header=include_header
                    )
                else:
                    results = params
                
        except Exception as e:
            raise QueryExecutionError(f'Error calling proc {proc_name}') from e
    
        return results
    
    async def get_pool_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics."""
        if not self.pool:
            return {}
        
        return {
            "size": self.pool.get_size(),
            "min_size": self.pool.get_min_size(),
            "max_size": self.pool.get_max_size(),
            "idle_size": self.pool.get_idle_size(),
        }
