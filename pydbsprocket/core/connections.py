from dataclasses import dataclass
from typing import Optional

@dataclass
class ConnectionConfig:
    host: str = ''
    port: Optional[int] = None
    database: str = ''
    username: str = ''
    password: str = ''
    schema: str = ''
    min_pool_size: int = 1
    max_pool_size: int = 5
    command_timeout: float = 60.0
    max_inactive_connection_lifetime: float = 300.0