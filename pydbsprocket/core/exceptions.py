class DatabaseProviderError(Exception):
    """Base exception for database provider errors."""
    pass

class ConnectionPoolError(DatabaseProviderError):
    """Raised when connection pool operations fail."""
    pass

class ConnectionError(DatabaseProviderError):
    """Raised when database connection fails."""
    pass

class QueryExecutionError(DatabaseProviderError):
    """Raised when query execution fails."""
    pass

class HealthCheckError(DatabaseProviderError):
    """Raised when database health check fails."""
    pass
